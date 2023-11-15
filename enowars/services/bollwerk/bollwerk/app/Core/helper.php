<?php

const ALLOW_LIST = [
    'files',
    'public',
    'View',
];

function resolvePath(string $path, array $allowedDirectories = ALLOW_LIST, bool $checkFileExistence = true): string
{
    if (!$checkFileExistence) {
        $basePath = explode('/', $path)[0] ?? '';

        if (str_contains($path, '..') || !in_array($basePath, $allowedDirectories)) {
            throw new RuntimeException("Could not find path $path");
        }

        return BASE_PATH . str_replace('/', DIRECTORY_SEPARATOR, $path);
    }

    $resolvedPath = realpath(BASE_PATH . str_replace('/', DIRECTORY_SEPARATOR, $path));

    if (!$resolvedPath) {
        throw new RuntimeException("Could not find path $path");
    }

    $baseDirectory = explode(DIRECTORY_SEPARATOR, explode(BASE_PATH, $resolvedPath)[1])[0];

    if (!in_array($baseDirectory, $allowedDirectories)) {
        throw new RuntimeException("Could not find path $path");
    }

    return $resolvedPath;
}
