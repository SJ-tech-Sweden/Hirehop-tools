 
# Hirehop-tools 
This project is for extending hirehop, I start with a new interface that works great to scan for check out on phones.
I will also add functionality to check in equipment and add other features.

For now you should only use it on your local firewalled network because there is no authentication whatsoever, that is something that I will add but wanted to get the basics to work first.

## Run Locally  

Clone the project  

~~~bash  
  git clone https://github.com/sjobergsson/Hirehop-tools
~~~

Create a copy config-example.yaml to config.yaml and add your hirehop token find according to https://www.hirehop.co.uk/api_documentation/#header-api-token

Create a django settings file

Migrate and create the superuser in the docker container, then restart the docker.
~~~bash  
  
  docker-compose down
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
