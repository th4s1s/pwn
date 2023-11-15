<?php

namespace Controller;

use Attributes\Route;
use Exception\NotFoundException;
use Exception\ValidationException;
use Http\Request;
use Http\Response;
use Http\View;
use Middleware\Authenticated;
use Model\Complaint;
use Request\CreateComplaintRequest;

readonly class SupportController
{
    #[Route(path: '/support', method: Request::POST, middlewares: [Authenticated::class])]
    public function store(Request $request, CreateComplaintRequest $createComplaintRequest): Response
    {
        try {
            $validated = $createComplaintRequest->validate();
        } catch (ValidationException $exception) {
            return View::render('support', ['errors' => $exception->errors]);
        }

        $token = $this->generateToken($request->session->getUser()->username);

        Complaint::create([
            'user_id' => $request->getCurrentUserId(),
            'description' => $validated['description'],
            'token' => $token,
            'submitted_at' => time(),
        ]);

        return Response::redirect('/support/' . $token);
    }

    private function generateToken(string $username): string
    {
        return base64_encode(sprintf("%-'_21s%.8s", $username, uniqid()));
    }

    #[Route(path: '/support')]
    public static function get(Request $request): Response
    {
        $complaints = Complaint::getAllByUser($request->getCurrentUserId());

        return View::render('support/index', [
            'complaints' => $complaints,
        ]);
    }

    #[Route(path: '/support-disclaimer')]
    public static function getDisclaimer(Request $request): Response
    {
        $complaints = Complaint::findAll();

        return View::render('support/disclaimer', [
            'complaints' => $complaints,
        ]);
    }

    #[Route(path: '/support/{token}')]
    public static function show(Request $request, string $token): Response
    {
        $complaint = Complaint::findOneBy(['token' => $token]);

        if ($complaint === null) {
            throw new NotFoundException();
        }

        return View::render('support/show', [
            'complaint' => $complaint,
        ]);
    }
}
