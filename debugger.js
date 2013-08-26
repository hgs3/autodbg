/*
Copyright (c) 2013 Henry G. Stratmann III

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
*/


function breakpoint(name) {
    name = (name == undefined || name == null) ? "unnamed" : name.toString();

    // This code launches our debugframe.py which communicates with our remote debugger.
    // You might be wondering why this is a string and why we eval() it.  The reason
    // is simple: In order to allow our debugger access to local variables, we
    // need to eval() the code rather than call it as a function().  Whatever is eval()'d
    // will exist in the same scope as the eval() itself.
    return "(function() {" +
        "var previousResult = undefined;" +
        "var CONTINUE_CMD = 'cont';" +
        "for(;;) {" +
            "try {" +
                "var result = UIATarget.localTarget().host().performTaskWithPathArgumentsTimeout('/usr/bin/env', ['python', '/usr/local/bin/debugframe.py', \"'\"+previousResult+\"'\", '" + name + "'], 60 * 10);" +
                "if (result.exitCode) {" +
                    "UIALogger.logDebug('Debugger error: ' + result.stderr);" +
                    "return;" +
                "}" +
                "if (result.stdout == CONTINUE_CMD) {" +
                    "return;" +
                "}" +
                "UIATarget.localTarget().pushTimeout(1);" +
                "var evalResult = eval(result.stdout);" +
                "UIATarget.localTarget().popTimeout();" +
                "if (evalResult) {" +
                    "previousResult = evalResult.toString();" +
                "}" +
                "else {" +
                    "previousResult = '(null)';" +
                "}" +
            "}" +
            "catch(error) {" +
                "previousResult = error;" +
            "}" +
        "}" +
    "})()";
}
