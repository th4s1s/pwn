<?php

namespace Request;

use Request\AbstractRequest;

class LoginRequest extends AbstractRequest
{
    public array $rules = [
        'username' => 'string->required|min:4|max:12',
        'password' => 'string->required|min:4|max:255',
    ];

    public array $messages = [
        'username' => 'Invalid username',
        'password' => 'Invalid password',
    ];
}
