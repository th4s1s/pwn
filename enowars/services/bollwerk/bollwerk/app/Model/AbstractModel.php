<?php

namespace Model;

use Core\App;
use Database\Database;
use ReflectionClass;

abstract class AbstractModel
{
    private static Database $database;

    protected static function getDatabase(): Database
    {
        if (!isset(static::$database)) {
            static::$database = App::resolve(Database::class);
        }

        return static::$database;
    }

    public static function find(int $id): ?static
    {
        $result = static::getDatabase()->fetchSingle('SELECT * FROM ' . static::getTableName() . ' where id = :id', [
            'id' => $id,
        ]);

        return $result ? static::hydrate($result) : null;
    }

    public static function findAll(): array
    {
        $result = static::getDatabase()->fetchAll('SELECT * FROM ' . static::getTableName());

        return $result ? static::hydrateMany($result) : [];
    }

    public static function findAllBy(array $parameters): array
    {
        $columns = array_map(static::convertToSnakeCase(...), array_keys($parameters));
        $parameterNames = array_map(static fn ($property) => ":$property", array_keys($parameters));

        $query = [];
        foreach ($columns as $index => $name) {
            $query[] = $name . ' = ' . $parameterNames[$index];
        }

        $result = static::getDatabase()->fetchAll(
            'SELECT * FROM ' . static::getTableName() . ' where ' . implode(' AND ', $query) . ' COLLATE NOCASE',
            $parameters
        );

        return $result ? static::hydrateMany($result) : [];
    }

    public static function findOneBy(array $parameters): ?static
    {
        $columns = array_map(static::convertToSnakeCase(...), array_keys($parameters));
        $parameterNames = array_map(static fn ($property) => ":$property", array_keys($parameters));

        $query = [];
        foreach ($columns as $index => $name) {
            $query[] = $name . ' = ' . $parameterNames[$index];
        }

        $result = static::getDatabase()->fetchSingle(
            'SELECT * FROM ' . static::getTableName() . ' where ' . implode(' AND ', $query) . ' COLLATE NOCASE',
            $parameters
        );

        return $result ? static::hydrate($result) : null;
    }

    public static function create(array $properties): static
    {
        $columns = array_map(static::convertToSnakeCase(...), array_keys($properties));
        $parameterNames = implode(', ', array_map(static fn ($property) => ":$property", array_keys($properties)));

        static::getDatabase()->execute(
            'INSERT INTO ' . static::getTableName() . '(' . implode(', ', $columns) . ') VALUES(' . $parameterNames . ')',
            $properties
        );

        return static::find(static::getDatabase()->getLastId());
    }

    public static function update(int $id, array $properties): static
    {
        $columns = array_map(static::convertToSnakeCase(...), array_keys($properties));
        $parameterNames = array_map(static fn ($property) => ":$property", array_keys($properties));

        $query = '';
        foreach ($columns as $index => $name) {
            $query .= $name . ' = ' . $parameterNames[$index];
        }

        static::getDatabase()->execute(
            'UPDATE ' . static::getTableName() . ' SET ' . $query . ' WHERE id = :id',
            ['id' => $id, ...$properties]
        );

        return static::find(static::getDatabase()->getLastId());
    }

    protected static function hydrateMany(array $result): array
    {
        return array_map(static::hydrate(...), $result);
    }

    protected static function hydrate(array $result): static
    {
        $model = new static();

        foreach (static::getPropertyNames() as $propertyName) {
            $value = static::convertToSnakeCase($propertyName);
            $model->$propertyName = $result[$value];
        }

        return $model;
    }

    private static function getPropertyNames(): array
    {
        $properties = (new ReflectionClass(static::class))->getProperties();

        return array_map(static fn($property) => $property->getName(), $properties);
    }

    protected static function getTableName(): string
    {
        return static::convertToSnakeCase((new ReflectionClass(static::class))->getShortName());
    }

    private static function convertToCamelCase(string $string): string
    {
        return lcfirst(str_replace('_', '', ucwords($string, '_')));
    }

    private static function convertToSnakeCase(string $string): string
    {
        return strtolower(preg_replace('/(?<!^)[A-Z]/', '_$0', $string));
    }
}