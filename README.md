# Pyramid Factory

Instantiate and distribute configuration for Pyramid based applications.

# Compatibility

Tool is developed for and tested with CentOS 7.

# Web setup
```
$ curl https://raw.githubusercontent.com/milos85vasic/Apache-Factory-Toolkit/master/websetup.py > websetup.py; \
python websetup.py Pyramid-Factory
```

# Hot to use
    
- Run as Super User by providing name of account to be created. 
Account will be created and Pyramid based application started for that user.
    
Distributing configuration:

- TBD.

## Account add with Apache Factory execution

```
$ su
$ mkdir Pyramid-Factory
$ cd Pyramid-Factory
$ git clone --recurse-submodules https://github.com/milos85vasic/Pyramid-Factory.git ./
$ python add_account.py YOUR_ACCOUNT_NAME
``` 

Script will start wizard that will for you create account, download, install and run Pyramid based application.

After whole process is completed you will be able to access landing page.

## Configuration parameters:

- Passing configuration for services

To tell Pyramid Factory which repositories to clone and configure make sure services.json is available in Pyramid Factory root.

Where services.json could look like this:
```
{
  "services": [
    {
      "url": "www.example.com",
      "urls": [
        "something.example.com",
        "something2.example.com"
      ],
      "repository": "https://github.com/user/some_repo.git"
    },
    {
      "url": "xxx.com",
      "repository": "other_git_repo ..."
    }
  ],
  "features": [
    "mysql"
  ]
}
```

To connect services (Pyramid based applications) with main proxy:
```
{
  "services": [
    {
      "main_proxy": "some_account",
      "url": "www.example2.com",
      "repository": "https://github.com/user/some_repo.git"
    },
    {
      "main_proxy": "some_account",
      "url": "www.example2.com",
      "repository": "https://github.com/user/some_repo.git"
    }
  ]
}
```

Where some_account represents account under which we initialized parent (main) proxy instance.

Note: Main proxy instance must be initialized and configured via [Apache Factory](https://github.com/milos85vasic/Apache-Factory).
