<?php

namespace Request;

use Http\Request;
use Validator\Validator;

abstract class AbstractRequest
{
    public array $rules = [];
    public array $messages = [];
    public array $data;

    public function __construct(
        public Request $request,
    ) {
        $this->data = [...$request->body, ...$request->queryParameters];
    }

    public function validate(): array
    {
        return Validator::validate($this->data, $this->rules, $this->messages);
    }
}
