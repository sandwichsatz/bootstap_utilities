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
        // Text with HTML content (e.g., this could be Django's `|safe` output)
        const text = `<p>Hello, <strong>this</strong> is <em>HTML</em> text!</p>`;

        const element = document.getElementById("typing-text");

        // Typing speed in milliseconds
        const typingSpeed = 100;

        // Function to extract characters and HTML tags separately
        function extractContentWithTags(htmlString) {
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = htmlString;
            const contentArray = [];

            function extractContent(node) {
                if (node.nodeType === Node.TEXT_NODE) {
                    // Split text nodes into individual characters
                    contentArray.push(...node.textContent.split(''));
                } else if (node.nodeType === Node.ELEMENT_NODE) {
                    // Add the opening tag
                    const openTag = `<${node.tagName.toLowerCase()}${Array.from(node.attributes).map(attr => ` ${attr.name}="${attr.value}"`).join('')}>`;
                    contentArray.push(openTag);

                    // Process child nodes recursively
                    Array.from(node.childNodes).forEach(extractContent);

                    // Add the closing tag
                    const closeTag = `</${node.tagName.toLowerCase()}>`;
                    contentArray.push(closeTag);
                }
            }

            // Start extracting from the top-level nodes
            Array.from(tempDiv.childNodes).forEach(extractContent);
            return contentArray;
        }

        // Function to "type" each character or tag part
        function typeText(contentArray) {
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

        // Extract and start typing
        window.onload = function() {
            const contentArray = extractContentWithTags(text); // Extract the HTML and characters
            typeText(contentArray); // Start typing character by character
        };
    </script>

</body>
</html>
