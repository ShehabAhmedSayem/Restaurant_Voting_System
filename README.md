# Restaurant_Voting_System
This is a voting system for a company to make a decision on lunch place.

### **Project Launch Instruction:**

1. Run the following command to start project using docker in detached mode
```
docker-compose up -d --build
```
2. Run this command to migrate the database
```
docker-compose exec web python manage.py migrate --noinput
```
3. Run this command to collect static files
```
docker-compose exec web python manage.py collectstatic
```
4. Run this command to create superuser. Then input username and password for the superuser.
```
docker-compose exec web python manage.py createsuperuser
```
5. Run this command to test the project.
```
docker-compose exec web python manage.py test
```

### **Api Documentation:**

The full api documentation can be found in the following url after launching the project:
```
http://127.0.0.1:8000/docs/
```

Project Use Case Instruction:

There are 3 types of users in this project:

`Admin : user_type=1`

`Employee : user_type=2`

`Restaurant_owner : user_type=3`

#### **1. Authentication**

The super user that was created during the launching step is an admin type of user.
Users can login through login api :

`http://127.0.0.1:8000/user/v1/login/`

Only admin type of user can create any type of user through register api :

`http://127.0.0.1:8000/user/v1/register/ `

#### **2. Creating restaurant**

Only admin type of user can create Restaurant_Owner type of user through register api :

`http://127.0.0.1:8000/user/v1/register/`

The value for `user_type` must be `3` for Restaurant_Owner.

Only Restaurant_Owner can create restaurant and upload menu for the restaurant.
Restaurant_Owner can create restaurant using this api :

`http://127.0.0.1:8000/voting/v1/restaurants/`

#### **3. Uploading menu for restaurant**

Only Restaurant_Owner can upload menu for his restaurants.
Restaurant_Owner can upload menu using this api :

`http://127.0.0.1:8000/voting/v1/menus/`

*Only one menu can be uploaded per day per restaurant.*

#### **4. Creating employee**

Only admin user can create employee user through register api :

`http://127.0.0.1:8000/user/v1/register/`

The value for `user_type` must be `2` for employee. 

#### **5. Getting current day menu**

Authenticated users can get the menu of current day through this api :

`http://127.0.0.1:8000/voting/v1/menus/?upload_date=2022-04-26`

Here the `upload_date` query parameter should be the current date.

#### **6. Voting for restaurant menu**

Only employee can vote for a menu through this api :

`http://127.0.0.1:8000/voting/v1/votes/`

*Employee can give only one vote per day. He can change his vote to another menu.*

Employee can update his vote through this api :

`http://127.0.0.1:8000/voting/v1/votes/{id}/`

*Voting increases num_of_votes property of menu model. Changing votes adjust the num_of_votes.*

#### **7. Getting results for the current day.**

Only admin user can publish result and stop voting through this api :

`http://127.0.0.1:8000/voting/v1/publish-result/`

*Voting must be stopped during publishing. After publishing employee cannot vote for that day. The winner restaurant will not be the winner for 3 consecutive working days.*

After publishing result any user can see the result of current day through this api :

`http://127.0.0.1:8000/voting/v1/result/?voting_date=2022-04-26`

Here the `upload_date` query parameter should be the current date.

#### **8. Logout**

User can logout through logout api :

`http://127.0.0.1:8000/user/v1/logout/`


