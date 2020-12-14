instructions = [
    'SET FOREIGN_KEY_CHECKS=0;',
    'DROP TABLE IF EXISTS user;',
    'DROP TABLE IF EXISTS recetas;',
    'SET FOREIGN_KEY_CHECKS=1',
    """
        CREATE TABLE user (
            id INT PRIMARY KEY AUTO_INCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(100) NOT NULL,
            nombre VARCHAR(50) NOT NULL,
            apellido VARCHAR(50) NOT NULL,
            sexo VARCHAR(50),
            correo VARCHAR(50) NOT NULL,
            permisos INT NOT NULL
        )
    """,
    """
        CREATE TABLE receta (
            id INT PRIMARY KEY AUTO_INCREMENT,
            titulo VARCHAR(50) NOT NULL,
            descripcion TEXT NOT NULL,
            ingredientes TEXT NOT NULL,
            preparacion TEXT NOT NULL,
            categoria VARCHAR(20) NOT NULL,
            url TEXT NOT NULL
        );
    """
]