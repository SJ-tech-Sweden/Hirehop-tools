# I have stopped using hirehop and started using eventory.se instead, so I won't redo this to work with the newer categories and I won't continue to develop it. If nobody else wan't to continue this project I will archive it in a few months. 
# Hirehop-tools 
This project is for extending hirehop, I start with a new interface that works great to scan for check out on phones.
I will also add functionality to check in equipment and add other features.

I have implemented django:s user authentication, if I continue work on the gui in this and not only using it for API and dashboards I will add possibility to authenticate with azuread saml.

## Run Locally  

### Clone the project  

~~~bash  
  git clone https://github.com/sjobergsson/Hirehop-tools
~~~

Create a copy config-example.yaml to config.yaml and add your hirehop token find according to https://www.hirehop.co.uk/api_documentation/#header-api-token

### Create a django settings file

### Migrate and create the superuser in the docker container, then restart the docker.
~~~bash
  docker-compose up -d  
~~~



## Contributing  

Contributions are always welcome!  
[Todo]
I will create a contributing document to help with contributing.

See `contributing.md` for ways to get started.  

Please adhere to this project's `code of conduct`.  

## License  

[MIT](https://choosealicense.com/licenses/mit/)
