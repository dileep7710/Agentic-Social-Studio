import json
from datetime import datetime
import ollama
from ddgs import DDGS
from social_tools import (
    post_instagram_feed,
    post_instagram_story,
    post_instagram_reel,
    post_facebook,
    post_whatsapp,
    broadcast_all_platforms
)

# ==================================================
# MEMORY
# ==================================================

MEMORY_FILE = "memory.json"


def load_memory():
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(memory, file, indent=4, ensure_ascii=False)


def add_memory(user_message, agent_message):
    memory = load_memory()
    memory.append({
        "user": user_message,
        "agent": agent_message
    })
    save_memory(memory)


# ==================================================
# PLANNER
# ==================================================

def planner(task):
    try:
        response = ollama.chat(
            model="llama3.2:3b",
            messages=[
                {
                    "role": "system",
                    "content": """
You are a task planner.
Create 2 to 5 short ACTION steps.
Do not answer the task.
Do not execute the task.
Return ONLY numbered action steps.

Example:
User: Broadcast this quote on all platforms: Amazing AI updates!
Output:
1. Generate 4K aesthetic quote image.
2. Publish to Instagram Story, Facebook, and WhatsApp simultaneously.
"""
                },
                {
                    "role": "user",
                    "content": task
                }
            ]
        )
        return response.message.content.strip()
    except Exception:
        return "1. Analyze task requirements.\n2. Execute necessary search / tools.\n3. Synthesize and deliver final result."


# ==================================================
# CONTENT EXTRACTION
# ==================================================

def extract_content(task):
    try:
        response = ollama.chat(
            model="llama3.2:3b",
            messages=[
                {
                    "role": "system",
                    "content": """
You extract the actual text/caption and any media file path or URL that the user wants to post.
Return ONLY the actual post content/caption.
Do NOT return:
- plan
- numbered steps
- platform names
- explanations
- instructions
- quotes around the content

Example:
User: Post this on Instagram: Today I learned how Agentic AI works.
Output:
Today I learned how Agentic AI works.
"""
                },
                {
                    "role": "user",
                    "content": task
                }
            ]
        )
        return response.message.content.strip()
    except Exception:
        return task


# ==================================================
# TOOL 1: CALCULATOR
# ==================================================

def calculator(a, b):
    return int(a) * int(b)


# ==================================================
# TOOL 2: TIME
# ==================================================

def get_time():
    return datetime.now().strftime("%H:%M:%S")


# ==================================================
# TOOL 3: WEB SEARCH
# ==================================================

def web_search(query):
    try:
        results = DDGS().text(query, max_results=5)
        if not results:
            return "No search results found."
        output = ""
        for result in results:
            output += (
                f"Title: {result.get('title', '')}\n"
                f"URL: {result.get('href', '')}\n"
                f"Summary: {result.get('body', '')}\n\n"
            )
        return output
    except Exception as e:
        return f"Web search error: {e}"


# ==================================================
# TOOL DEFINITIONS FOR LLAMA
# ==================================================

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Multiply two numbers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "integer"},
                    "b": {"type": "integer"}
                },
                "required": ["a", "b"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "Get the current local time.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the internet for current information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "broadcast_all_platforms",
            "description": "Broadcast a 4K Nature Quote Graphic simultaneously across Instagram Story, Facebook, and WhatsApp in one single command.",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "The quote or message content to post on all platforms."},
                    "whatsapp_phone": {"type": "string", "description": "Optional WhatsApp phone number (e.g. +919876543210)."}
                },
                "required": ["content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "post_instagram_feed",
            "description": "Publish a permanent feed post with image and caption to Instagram. Supports web image URLs and local PC image paths.",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {"type": "string"},
                    "media_path_or_url": {"type": "string", "description": "Optional local file path or web URL for the photo."}
                },
                "required": ["content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "post_instagram_story",
            "description": "Publish a 24-hour Story to Instagram. Supports web image URLs and local PC image paths.",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {"type": "string"},
                    "media_path_or_url": {"type": "string", "description": "Optional local file path or web URL for the story image."}
                },
                "required": ["content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "post_instagram_reel",
            "description": "Publish an Instagram Reel or Video post. Supports web video URLs and local PC video files (.mp4).",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "Caption / description for the reel."},
                    "video_path_or_url": {"type": "string", "description": "Optional local video path (.mp4) or web URL."}
                },
                "required": ["content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "post_facebook",
            "description": "Publish content to Facebook.",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {"type": "string"}
                },
                "required": ["content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "post_whatsapp",
            "description": "Send a real WhatsApp message to a phone number or contact via WhatsApp Web.",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "The message text to send."},
                    "target": {"type": "string", "description": "Optional phone number with country code (e.g. +919876543210)."}
                },
                "required": ["content"]
            }
        }
    }
]


# ==================================================
# MAIN ENTRY POINT
# ==================================================

def main():
    print("======================================")
    print("       AGENTIC AI ASSISTANT")
    print("======================================")
    print("Type 'exit' to stop.")

    while True:
        user_question = input("\nYou: ").strip()

        if not user_question:
            continue

        if user_question.lower() in ["exit", "quit", "bye"]:
            print("Agent: Goodbye!")
            break

        # 1. Load memory
        memory = load_memory()
        memory_text = ""
        for item in memory[-10:]:
            memory_text += f"User: {item['user']}\nAgent: {item['agent']}\n\n"

        # 2. Planner
        print("\nThinking...")
        plan = planner(user_question)
        print("\n========== PLAN ==========")
        print(plan)

        # 3. Extract content (if it's a posting task)
        content = extract_content(user_question)
        print("\n========== CONTENT ==========")
        print(content)

        # 4. Prepare system prompt & messages
        messages = [
            {
                "role": "system",
                "content": f"""
You are an autonomous AI agent.

Available tools:
calculator
get_time
web_search
broadcast_all_platforms
post_instagram_feed
post_instagram_story
post_instagram_reel
post_facebook
post_whatsapp

USER TASK:
{user_question}

ACTUAL USER CONTENT:
{content}

PLAN:
{plan}

PREVIOUS MEMORY:
{memory_text}

IMPORTANT RULES:
1. Follow the user's original task.
2. If the user asks to broadcast/post on ALL platforms (Instagram + Facebook + WhatsApp), call broadcast_all_platforms.
3. If the user asks for Instagram Reel / Video, call post_instagram_reel.
4. If the user asks for Instagram Story, call post_instagram_story.
5. If the user asks for Instagram post / feed, call post_instagram_feed.
6. If Facebook is requested, call post_facebook.
7. If WhatsApp is requested, call post_whatsapp.
8. Pass any media file path or URL mentioned in the task as media_path_or_url or video_path_or_url.
9. When posting, ALWAYS use the ACTUAL USER CONTENT.
10. NEVER use the planner steps as the social media content.
11. Do not invent content.
12. Continue until all requested platforms are completed.
13. After all required tools finish, provide a short final report.
"""
            },
            {
                "role": "user",
                "content": user_question
            }
        ]

        # 5. Agent loop
        max_iterations = 10
        iteration = 0

        while iteration < max_iterations:
            iteration += 1
            print(f"\n----- Agent iteration {iteration} -----")

            response = ollama.chat(
                model="llama3.2:3b",
                messages=messages,
                tools=tools
            )

            messages.append(response.message)

            # If no tool calls -> Final answer
            if not response.message.tool_calls:
                final_answer = response.message.content
                print("\n========== FINAL ANSWER ==========")
                print(final_answer)
                add_memory(user_question, final_answer)
                break

            # Execute tool calls
            for tool_call in response.message.tool_calls:
                function_name = tool_call.function.name
                arguments = tool_call.function.arguments

                print("\n========== TOOL ==========")
                print("Selected:", function_name)
                print("Arguments:", arguments)

                actual_text = arguments.get("content") or content
                media_arg = arguments.get("media_path_or_url") or arguments.get("video_path_or_url")

                if function_name == "calculator":
                    try:
                        result = calculator(int(arguments["a"]), int(arguments["b"]))
                    except Exception as e:
                        result = f"Calculator error: {e}"

                elif function_name == "get_time":
                    result = get_time()

                elif function_name == "web_search":
                    result = web_search(arguments.get("query", user_question))

                elif function_name == "broadcast_all_platforms":
                    result = broadcast_all_platforms(
                        content=actual_text,
                        whatsapp_phone=arguments.get("whatsapp_phone") or arguments.get("target")
                    )

                elif function_name == "post_instagram_feed":
                    result = post_instagram_feed(actual_text, media_arg)

                elif function_name == "post_instagram_story":
                    result = post_instagram_story(actual_text, media_arg)

                elif function_name == "post_instagram_reel":
                    result = post_instagram_reel(actual_text, media_arg)

                elif function_name == "post_facebook":
                    result = post_facebook(actual_text)

                elif function_name == "post_whatsapp":
                    result = post_whatsapp(actual_text, arguments.get("target"))

                else:
                    result = "Unknown tool."

                print("\n========== TOOL RESULT ==========")
                print(result)

                messages.append({
                    "role": "tool",
                    "tool_name": function_name,
                    "content": str(result)
                })

                print("\nTool result sent back to Llama...")

        else:
            print("\nAgent: Maximum agent steps reached.")


if __name__ == "__main__":
    main()