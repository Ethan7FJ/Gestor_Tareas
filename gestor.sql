-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 21-05-2024 a las 19:18:07
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `gestor`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tareas`
--

CREATE DATABASE gestor
    DEFAULT CHARACTER SET = 'utf8mb4';

USE gestor;

CREATE TABLE `tareas` (
  `id_t` int(11) NOT NULL,
  `nombre_t` varchar(50) NOT NULL,
  `fecha_inicio_t` date DEFAULT NULL,
  `fecha_final_t` date DEFAULT NULL,
  `estado` varchar(50) NOT NULL,
  `id_u` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tareas`
--

INSERT INTO `tareas` (`id_t`, `nombre_t`, `fecha_inicio_t`, `fecha_final_t`, `estado`, `id_u`) VALUES
(6, 'Jugar fornais', '2024-05-21', '2024-05-21', 'En proceso', 3),
(8, 'Todoo', '2024-05-29', '2024-05-22', 'En proceso', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_u` int(11) NOT NULL,
  `nombre_u` varchar(50) NOT NULL,
  `apellido_u` varchar(50) NOT NULL,
  `email_u` varchar(50) NOT NULL,
  `usuario_u` varchar(50) NOT NULL,
  `contrasena_u` varchar(255) NOT NULL,
  `rol_u` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_u`, `nombre_u`, `apellido_u`, `email_u`, `usuario_u`, `contrasena_u`, `rol_u`) VALUES
(1, 'Kamildo', 'Fetecua', 'kami@gmail.com', 'Kamil', 'scrypt:32768:8:1$4HbWG0hbZNchtfRJ$bce236b79a842d80a79c2883f08e6c0a192e729cddf9863df041d82602116810db1d8d82f67093cd9f4d95c452ad7ec6f4b5227186e7ff15a92c89698b7eb2cb', 'Admin'),
(3, 'Sebas', 'Gacha', 'sg@gmal.com', 'Carlitos', 'scrypt:32768:8:1$FRwAjmlfbDSk8Cp2$d56c8fb0aef436c498f6f15150f913f305d041ecb57cda96df30267776cd0dac1a861a285919b96a85f19aef0bae11fb57aafee0aaf1ea0633ae7c9301489ce1', 'Usuario'),
(4, 'Jojam', 'fetescua', 'johanrfetecua@gmail.com', 'Jogan', 'scrypt:32768:8:1$D03wJVtTTfBpGFxd$30ad900a81fc65d2e33e8973567ed59a6775dfc21616f8b4edeed63386b70273e212bee4ba44d9ddacd54a1bab80f48301c8826106be416571d576ec96602f00', 'Usuario'),
(5, 'Julian', 'Rey', 'Jr@gmail.com', 'Julis', 'scrypt:32768:8:1$H9lWjjscR8IobtXJ$e94e9ac90e51f8b44178d2ff6866498a171b9f5925086bf9ff8efaa05b68bcbea1f07ef3a9ad2c4df35b05ea41f303be8adc9403b4634385b60958624da6d838', 'Usuario');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `tareas`
--
ALTER TABLE `tareas`
  ADD PRIMARY KEY (`id_t`),
  ADD KEY `id_u` (`id_u`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_u`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `tareas`
--
ALTER TABLE `tareas`
  MODIFY `id_t` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_u` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `tareas`
--
ALTER TABLE `tareas`
  ADD CONSTRAINT `tareas_ibfk_1` FOREIGN KEY (`id_u`) REFERENCES `usuarios` (`id_u`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;


SELECT id_u FROM usuarios WHERE id_u;
SELECT id_u FROM usuarios;