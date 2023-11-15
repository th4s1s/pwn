<?php

namespace Validator;

use Exception\ValidationException;
use RuntimeException;

class Validator
{
    public static function validate(array $data, array $rules, array $messages): array
    {
        $validated = [];
        $errors = [];

        foreach ($rules as $key => $rule) {
            if (array_key_exists($key, $data)) {
                if (self::validateRule($data[$key], $rule)) {
                    $validated[$key] = $data[$key];
                    continue;
                }
                $errors[$key] = $messages[$key] ?? 'Invalid value';
            }

            if (self::validateRule(null, $rule)) {
                continue;
            }

            $errors[$key] = $messages[$key] ?? 'Invalid value';
        }

        if (count($errors) > 0) {
            throw new ValidationException($errors);
        }

        return $validated;
    }

    private static function validateRule(mixed $value, string $rule): bool
    {
        $parameters = explode('->', $rule);

        if ($value === null && count($parameters) > 1) {
            $rules = explode('|', $parameters[1]);
            if ($rules[0] === 'optional') {
                return true;
            }
        }

        if (!self::validateType($value, $parameters[0])) {
            return false;
        }

        if (count($parameters) <= 1) {
            return true;
        }

        $rules = explode('|', $parameters[1]);

        foreach ($rules as $rule) {
            if (is_string($value)) {
                if (!self::validateString($value, $rule)) {
                    return false;
                }

                continue;
            }

            if (is_int($value)) {
                if (!self::validateInt($value, $rule)) {
                    return false;
                }

                continue;
            }

            throw new RuntimeException('Can not validate type ' . gettype($value));
        }

        return true;
    }

    private static function validateType(mixed $value, string $type): bool
    {
        return match ($type) {
            'string' => is_string($value),
            'int' => is_int($value),
            default => throw new RuntimeException("Unknown type $$type"),
        };
    }

    private static function validateInt(int $value, string $rule): bool
    {
        $options = explode(':', $rule);

        $rule = $options[0];

        return match ($rule) {
            'optional' => true,
            'equals' => $value === (int)self::getOption($options),
            'max' => $value <= (int)self::getOption($options),
            'min' => $value >= (int)self::getOption($options),
            default => throw new RuntimeException("Unknown rule $rule for type int"),
        };
    }

    private static function validateString(string $value, string $rule): bool
    {
        $options = explode(':', $rule);

        $rule = $options[0];
        return match ($rule) {
            'optional' => true,
            'required' => $value !== '',
            'empty' => $value === '',
            'equals' => $value === self::getOption($options),
            'max' => mb_strlen($value) <= self::getOption($options),
            'min' => mb_strlen($value) >= self::getOption($options),
            default => throw new RuntimeException("Unknown rule $rule for type string"),
        };
    }

    private static function getOption(array $options): string
    {
        if (count($options) !== 2) {
            throw new RuntimeException("Could not get option for rule $options[0]");
        }

        return $options[1];
    }
}