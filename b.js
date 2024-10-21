<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Typing Effect with Safe HTML</title>
    <style>
        .typing-effect {
            font-size: 24px;
            font-family: 'Courier New', Courier, monospace;
        }
    </style>
</head>
<body>

    <!-- HTML content with safe filter -->
    <div class="typing-effect" id="typing-text"></div>

    <script>
        // Text with HTML content (which would typically be outputted by Django with |safe)
        const text = `<p>Hello, <strong>this</strong> is <em>HTML</em> text!</p>`;

        const element = document.getElementById("typing-text");

        // Typing speed in milliseconds
        const typingSpeed = 100;

        // This function extracts content and ensures the HTML structure is maintained
        function typeText(htmlString) {
            // Create a temporary element to hold the HTML
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = htmlString;

            // Array to store the content
            const contentArray = [];

            // Recursively extract the text nodes and HTML tags
            function extractContent(node) {
                if (node.nodeType === Node.TEXT_NODE) {
                    contentArray.push(node.textContent); // Add text content
                } else if (node.nodeType === Node.ELEMENT_NODE) {
                    const openTag = `<${node.tagName.toLowerCase()}${Array.from(node.attributes).map(attr => ` ${attr.name}="${attr.value}"`).join('')}>`;
                    const closeTag = `</${node.tagName.toLowerCase()}>`;
                    contentArray.push(openTag);
                    Array.from(node.childNodes).forEach(extractContent);
                    contentArray.push(closeTag);
                }
            }

            // Start extracting content
            Array.from(tempDiv.childNodes).forEach(extractContent);

            // Initialize typing
            let index = 0;
            function typeCharacter() {
                if (index < contentArray.length) {
                    element.innerHTML += contentArray[index];
                    index++;
                    setTimeout(typeCharacter, typingSpeed);
                }
            }

            typeCharacter();
        }

        // Call the function with the HTML string
        window.onload = function() {
            typeText(text);
        };
    </script>

</body>
</html>
