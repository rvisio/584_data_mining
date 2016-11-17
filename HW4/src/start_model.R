library(dplyr)
library(xgboost)
library(stats)
library(class)
library(FNN)

train<-read.table("H:/hw4/train.dat",sep="",header=T)
test<-read.table("H:/hw4/test.dat",sep="",header=T)

movie_list<-unique(train$movieID)
movie_id_ratings<-train %>% group_by(movieID) %>% summarise(mean_movie=mean(rating),sd=sd(rating),n=n(),median_movie=median(rating))

users<-train %>% group_by(userID) %>% summarise(avg_rating=mean(rating),rating_var=sd(rating),med_rating=median(rating),movies_rated=n())
train.x<-merge(train,movie_id_ratings,by="movieID",all.x=T)
train.x<- train.x %>% arrange(userID)
train.x<-merge(train.x,users,by="userID",all.x=T)
train.x<-train.x %>% mutate(rating_diff = rating-median_movie,under_median= ifelse(rating_diff < 0,1,0))
train.x<-train.x %>% group_by(userID) %>% mutate(negative_nacy=sum(under_median)/n())
train.x_NN<-train.x %>% select(userID,negative_nacy) %>% summarise(NN=mean(negative_nacy))
users_knn<-merge(users,train.x_NN,all.x=T)
usersID<-users_knn$userID
users_knn<-users_knn[-1]
users_knn<-scale(users_knn) #standardize for KNN
indices_list<-c()
for(i in 1:nrow(users_knn)){
  knn_users_out<-knn(users_knn,users_knn[i,],usersID,k=10,algorithm="cover_tree")
  indices<-attr(knn_users_out,"nn.index")
  indices_list<-rbind(indices_list,indices)
}
indices_list<-data.frame(indices_list)
indices_list_ids<-cbind(usersID[indices_list$X1],usersID[indices_list$X2],usersID[indices_list$X3],
                        usersID[indices_list$X4],usersID[indices_list$X5],usersID[indices_list$X6],
                        usersID[indices_list$X7],usersID[indices_list$X8],usersID[indices_list$X9],
                        usersID[indices_list$X10])
indices_list_ids<-data.frame(indices_list_ids)

write.csv(indices_list_ids,"H:/hw4/knn_match.csv",row.names=F)
knn_movies<-read.table("H:/hw4/knn_movie_prediction.dat",sep=" ",header=F)

knn_movies<-unique(knn_movies)


#train.x<-merge(train.x,knn_movies,by.x="movieID",by.y="V1",all.x=T)
train.x<-merge(train.x,knn_movies,by.x="movieID",by.y="V1",all.x=T)
train.x_ratings<-train.x$rating
train.x$rating<-NULL
train.x$under_median<-NULL
train.x$rating_diff<-NULL

x<-xgb.DMatrix(data=data.matrix(train.x),label=train.x_ratings,missing=NaN)
model<-xgb.cv(data = x, 
              booster="gblinear",
              objective = "reg:linear", 
              max.depth = 5, 
              nround = 500, 
              lambda = 0, 
              lambda_bias = 0, 
              alpha = 0,
              nfold=5,
              eta=0.1)

model2<-xgboost(data = x, 
                booster="gblinear",
                objective = "reg:linear", 
                max.depth = 5, 
                nround = 240, 
                lambda = 0, 
                lambda_bias = 0, 
                alpha = 0,
                eta=0.1)

test.x<-merge(test,movie_id_ratings,by="movieID",all.x=T)
test.x<- test.x %>% arrange(userID)
test.x<-merge(test.x,users,by="userID",all.x=T)
test.x$rating_diff<-NULL
test.x_ratings<-test.x$rating
test.x$rating<-NULL
test.x$rating_diff<-NULL
test.x<-merge(test.x,knn_movies,by="movieID",by.y="V1",all.x=T)

pred<-predict(model2,data.matrix(test.x),missing=NaN)
pred3<-predict(model2,data.matrix(train.x),missing=NaN)

#RMSE #CV
for_rmse<-data.frame(pred3,train.x_ratings)

overallMean<-mean(train$rating)
movieMeans<-aggregate(rating~movieID,data=train,mean)
movieRating<-movieMeans[train$movieID,"rating"]

for_rmse$pred3<-ifelse(for_rmse$pred3<0.5,.5,ifelse(for_rmse$pred3>5,5,for_rmse$pred3))

j<-c()
for(i in 1:100){
  y<-i/100
  print(y)
  for_rmse$pred4<-y*for_rmse$pred3+(1-y)*movieRating
  q<-sqrt(mean((for_rmse$pred4-for_rmse$train.x_ratings)^2,na.rm=T))
  j<-rbind(j,q)
}
which.min(j)

#Graph
library(gridExtra)
library(ggplot2)
pred<-data.frame(pred)
a<-ggplot(data=pred,aes(x=pred))+geom_histogram(color="black")+theme_minimal()+ggtitle("Final Predictions")
b<-ggplot(data=train,aes(x=rating))+geom_histogram(color="black")+theme_minimal()+ggtitle("Train Predictions")
grid.arrange(a,b,ncol=2)

pred$pred<-ifelse(pred$pred< 0.5,.5,ifelse(pred$pred > 5,5,pred$pred))

write.csv(pred$pred,"H:/hw4/out.csv",row.names=F)