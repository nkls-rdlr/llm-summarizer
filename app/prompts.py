format_prompt = """
You are provided with a large string object that is a transcript of a video. The string is one continuous line without any formatting. Your task is to format this string into a Markdown file. Here are the specific instructions:
- Preserve Content: Do not alter, add, or remove any content from the original string. The text must remain exactly the same.
- Newlines: Insert newlines where appropriate to create readable sentences and paragraphs.
- Paragraphs: Group related sentences into paragraphs. Each paragraph should be separated by a blank line.
- Markdown Formatting: Ensure the final output is in Markdown format.
- Links: Do NOT include any URLs that might lead to websites, even if they are mentioned in the transcript.
Please format the following transcript accordingly:
"""

summarize_prompt = """
Summarize the following transcript in a structured format using clear topics and bullet points.
- The summary should be easy to understand, with each topic having a brief heading followed by concise bullet points outlining the key details.
- While staying concise, make sure to add enough detail so that the content can easily be understood by someone reading it for the first time.
- Structure the content logically based on its meaning to ensure a coherent and intuitive flow. Do not add extra comments or explanations (e.g. "Here is a summary...:"), just return the summary.
- Format the summary in Markdown.
Here is the transcript: 
"""
