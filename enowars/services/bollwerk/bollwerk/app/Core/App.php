<?php

namespace Core;

use Core\ServiceContainer;

class App
{
    private static ServiceContainer $container;

    public static function setContainer($container): void
    {
        static::$container = $container;
    }

    public static function getContainer(): ServiceContainer
    {
        return static::$container;
    }

    public static function resolve(string $key)
    {
        return static::$container->get($key);
    }
}