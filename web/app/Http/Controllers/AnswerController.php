<?php

namespace App\Http\Controllers;
use Illuminate\Http\Request;

class AnswerController extends Controller
{
    /**
     * Create a new controller instance.
     *
     * @return void
     */

    public function index($question)
    {
        exec('python ../../qa.py ' . escapeshellarg($question), $result);
        $result = join("\n\n", $result);
        return ["answer" => $result];
    }
}
