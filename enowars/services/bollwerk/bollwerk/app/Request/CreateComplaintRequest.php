<?php

namespace Request;

use Validator\Validator;

class CreateComplaintRequest extends AbstractRequest
{
    public array $rules = [
        'description' => 'string->min:1|max:255',
    ];

    public array $messages = [
        'description' => 'Please provide a description at most 255 characters',
    ];

    public function validate(): array
    {
        return Validator::validate($this->data, $this->rules, $this->messages);
    }
}
