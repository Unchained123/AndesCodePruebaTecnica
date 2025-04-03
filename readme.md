1. Clonar el repositorio
2. Ejecutar "pip install -r requirements.txt" para instalar requerimientos
3. Si la base de datos no esta creada, ejecutar archivo create_db.py 
4. Ejecutar api.py

Preguntas y Respuestas.
Seguridad: 
¿Qué medidas básicas implementarías para proteger esta API?
Para proteger la api se podria implementar autenticación para el uso de la api, encriptacion de la base de datos, registrar los eventos y errores en logs para que el cliente reciba la menor informacion posible de la api, uso de certificado ssl para el trafico http. Creo que ya esta implementado pero tambien usar proteger la api contra inyecciones SQL.

¿Cómo gestionarías la autenticación de usuarios? 
Para la autenticacion de usuarios permitiria que los usuarios creen una cuenta con usuario y contraseña. La contraseña la almacenaria hasheada para protegerla de accesos no autorizados a la base de datos. Una vez que el usuario se autentica se le daria un token jwt el cual necesitará para poder hacer uso de la api, este token tendria una expiracion luego de un tiempo, tambien permitiria la renovacion del token para que el usuario no deba iniciar sesion cada vez que el token expire.

DevOps:
¿Qué herramientas usarías para desplegar esta app en un entorno productivo?
Utilizaria Gunicorn como servidor de puerta de enlace, este podria manejar varias instancias de la aplicacion, reiniciarlas si fallan y balancear carga. Luego utilizaria nginx como proxy inverso a traves del cual podria implementar SSL. Como proveedor de nube podria utilizar AWS EC2 o Google Cloud App Engine, que darían la infraestructura necesaria para ejecutar los servicios mencionados. 