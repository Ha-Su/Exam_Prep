import google.generativeai as genai

genai.configure(api_key="AIzaSyD_zK_-MrOgNAtML2MuiRZW4ibbXt83G1I")

question1 = """
I have a pair of question and answer :
"question": "Was sagt Helmholtz’s theory of unconscious inference aus? Zeichne ein Beispiel.",
"answer": "Helmholtz's theory of unconscious inference suggests that the brain makes the \"best possible interpretation of the stimulus\" 
based on past experiences and knowledge. Essentially, our perception is not a direct reading of sensory input, but rather an active 
inference or guess about the causes of that input.\n\nHere's a simplified example:\n\nImagine you are walking in a park and see a blurry, 
brown shape on the ground.\n\n*   **Sensory Input:** Blurry, brown shape.\n*   **Unconscious Inference (Helmholtz's theory):** Your brain, 
drawing on past experiences, unconsciously infers that this shape is most likely a fallen leaf. It \"chooses\" this 
interpretation because, given the visual cues (blurry, brown), it's the most probable cause given your prior knowledge of parks.\n\n**Drawing Example:**\n\nYou could draw this by showing:\n\n1.  **A blurry brown blob:** Representing the raw sensory input.\n2.  **An arrow pointing from the blob to:**\n    *   A drawing of a **fallen leaf**.\n    *   (Optionally, you could add fainter arrows to less likely interpretations like a piece of wood or a discarded wrapper, to emphasize that the leaf is the \"best possible interpretation\").\n\nThis illustrates how the brain goes beyond the raw data to construct a meaningful perception.",


Take for example this is an exam, and the QnA pair is the question and answer in the exam. and the question itself gives 2 points, 1 for each correct answer (definition and example).
Grade the following answer give by someone, be strict and also explain very shortly what is wrong with the answer.
The grading should stick to the actual QnA pair, although you can be a bit lenient, but it still needs to uphold the actual QnA pair.

Given answer :
Helmholtz theory of unconscious inference states that perception is the result of unconcsious assumption based on past experiences.
For example : Imagine 2 squares that looks like they're overlapping on one of the edges, our brain assumes that it is overlapping eventhough the shape might not even be squares but just a weirdly shaped object that makes it looks like they are overlapping.
"""

question2 = """
In HCI we have a concept called dark design pattern, they are : Nagging, Obstruction, Interface interference, forced action, sneaking.
They all have defintions and examples. Imagine that you are a professor in HCI and making questions for exams regarding this.
Make 3 pairs of question and answers out of it.
"""

question3 = """
can you explain this snippets from a HCI lecture?
Explain explicitly and strictly only from what I send you below, how do you interpret it

## Within-Subject Design:

## Between-Subject Design:

- Each participant is exposed to all experimental conditions.
- Only one group of participants is needed for the entire experiment.
+ Smaller number of participants needed for the same amount of data.
+ Smaller influence of interpersonal differences. - Learning effects between conditions*
- Each participant is only exposed to one experimental condition.
- The number of participant groups directly correspond to the number of experimental conditions.
+ Simple Design
+ Low influence of fatigue (or other effects that appear over time)
- Large number of participants needed.
- Impact of interpersonal differences.
* For example: participant may perform better when subsequently completing the same tasks using another interface.
"""

question4 = """
You are a professor in HCI. You have this definitions :
Here's a brief explanation of those HCI concepts:

*   **Helmholtz's Theory of Unconscious Inference:** Our brains constantly make educated guesses (inferences) about the world based on incomplete sensory information and past experiences. These inferences happen so quickly and automatically that we're not consciously aware of them. In HCI, this means users often fill in missing information or interpret ambiguous elements based on their existing knowledge, and interfaces should leverage this.

*   **Gestalt Laws of Perception:** These are principles describing how humans naturally organize visual elements into unified wholes.
    *   **Proximity:** Objects close together are perceived as a group.
    *   **Similarity:** Objects that look alike are perceived as a group.
    *   **Continuity:** Elements arranged on a line or curve are perceived as more related than elements not on the line or curve.
    *   **Closure:** We tend to perceive incomplete figures as complete by filling in the missing gaps.
    *   **Common Fate:** Objects moving in the same direction are perceived as a group.
    *   **Figure/Ground:** We perceptually divide our visual field into a figure (object of focus) and a ground (background).

*   **Distributed Cognition / Extended Mind Theory:** Cognition (thinking, learning, remembering) isn't confined solely within an individual's brain. It can be distributed across the mind, body, and the external environment, including tools, artifacts, and other people. In HCI, this highlights how interfaces and technologies become integrated parts of our cognitive processes, extending our mental capabilities.

Now you are holding an exam. One of the question in the exam is :
What is the Helmholtz' Theory of Unconscious Inference? Explain.

A student answered with :
Helmholtz theory of unconscious inference states that perceptions are the results of unconcious assumptions based on past experiences.

Grade this answer based on the actual defintion that is given. As a professor how would you grade it? Is it an acceptable answer? 
The maximum grade for this question is 2 points.
"""

model = genai.GenerativeModel("gemini-2.5-flash-lite-preview-06-17") 
response = model.generate_content(question3)
print(response.text)