def extract_defended_position(text: str) -> str:
    return f"""
        Read this paragraph and identify, in one sentence, the position defended by the Target Speaker

        Text: Target Speaker: In the contemporary landscape of our interconnected world, the urgent need 
        for sustainable development is paramount. Prioritizing the adoption of clean energy technologies, 
        responsible resource management, and fostering international collaboration can collectively pave the 
        way for a greener and more resilient future. Addressing environmental challenges and combating climate 
        change requires a concerted effort on a global scale.
        Answer: the Target Speaker advocates for global cooperation, clean energy adoption, and responsible 
        resource management to address environmental challenges and combat climate change.


        Text: {text}
        Answer
    """

def extract_speech_quality_report(text: str, defended_position: str) -> str:
    return f"""
        You are a speech reviewer in charge of evaluating the quality of the arguments of a Target Speaker. Your input is a
        conversation with a Target Speaker, where he shares several arguments to back up his opinion, followed up but said 
        opinion (After the title "Target Speaker Opinion:").

        Your task is to create a Markdown document with an analysis of the arguments used by the Target Speaker to support his opinion,
        following the steps below:
        1. Identify the use of fallacies by the Target Speaker when supporting his opinion.
        2. Identify the use of wrong arguments by the Target Speaker when supporting his opinion, according to mathematical logic and definitions.
        3. Identify the use of diverging arguments by the Target Speaker when supporting his opinion, that do not address the question or comment at hand.
        4. Identify arguments said by the Target Speaker to support his opinion that are not backed up by evidence or data.
        5. Identify the use of personal projections not backed up by evidence but by a personal opinion.

        Text: {text}\nTarget Speaker Opinion: {defended_position}
        Answer:
    """

def prettify_to_markdown(text: str) -> str:
    return f"""
        Your task is to re-write the text below using Markdown, without changing the semantic of the text.
        
        {text}
    """
