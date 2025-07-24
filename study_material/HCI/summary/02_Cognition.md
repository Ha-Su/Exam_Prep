# Cognition and Perception

## Cognition
- **Cognition**: the mental processes such as perception, attention, memory, and so on, that are what the mind does. (Slide 6)  
- **Mind**: a system that creates representations of the world so that we can act to achieve our goals; controls mental functions such as perception, attention, memory, emotions, language, thinking, and reasoning. (Slide 6)  
- **Cognitive Psychology**: the branch of psychology concerned with the scientific study of the mind. (Slide 6)  

## Model Human Processor
- **Three subsystems**:  
  1. Sensory input subsystem  
  2. Central information processing subsystem  
  3. Motor output subsystem  
  (Slides 10-11)  
- **Limitations**: omits the body, context, emotions, and social aspects of human behavior. (Slide 11)  
- **Application**: can “calculate” how long simple tasks take; basis for GOMS (Goals, Operators, Methods, Selection rules) and KLM (Keystroke-Level Model). (Slide 12)  
- **Historical view**: Disembodied cognition ("I think therefore I am") (Slide 9)  

## Memory
- **Sensory Memory**: exists for each channel (iconic, echoic, haptic); information passes to short-term memory via attention. (Slide 13)  
- **Working/Short-Term Memory**: a “scratch-pad” for temporary information; accessed in ~70 ms, decays in ~200 ms; capacity of 7 ± 2 chunks. (Slides 13-15)  
- **Long-Term Memory**: stores everything we “know” (episodic and semantic); large capacity; access time ~0.1 s; forgetting occurs slowly. (Slide 13)  
- **7±2 Rule Application**: Critical for command-line interfaces (holding parameters in memory), but misapplied when used to limit menu lengths (menus act as external cues). (Slide 15)  

## Situated Action
- **Principle**: human action cannot be fully captured by formal plans; must observe users in context. (Slide 18)  
- **Example**: Lucy Suchman’s Xerox PARC study on copier use laid groundwork for human-centered design and context-aware systems. (Slide 18)  
- **Key insight**: People don't follow simple plans; behavior must be observed in context. (Slide 18)  

## Distributed Cognition & Extended Mind
- **Distributed Cognition**: cognitive processes and knowledge distributed across people, tools, and representations; distinguishes internal vs. external representations. (Slide 21)  
- **Extended Memory**: e.g., maps/notes (Slide 21)  
- **Extended Processes**: e.g., speed displays/calculators (Slide 21)  
- **Extended Mind Theory**: technology (e.g., smartphones) can replace parts of mind/memory, shifting emphasis to good interface design. (Slide 21)  
- **Implications**: Impacts social life, education (exams), and essential skills (using tools like ChatGPT). (Slide 21)  

## Embodied Cognition & Affordances
- **Embodied Cognition**: cognition arises from our brains, bodies, and bodily experiences; body influences the mind. (Slide 23)  
- **Affordances** (Gibson 1977): properties of an artifact that indicate possible uses; when good, no labels needed. (Slides 24, 30)  
- **Perceived Affordances** (Norman): what users believe they can do with an object, guiding actions. (Slide 24)  
- **Types of Affordances** (Gaver 1991):  
  - Perceptible : Perceptual characteristics of the object itself indicate what action possibilities are available and desired  (e.g., door handle)  
  - Hidden : Users often must rely on experience and/or trial and error to determine possible action (e.g., undiscovered menus)  
  - False : An object's characteristics suggest users can do something they can't (e.g., underlined non-link text)  
  (Slide 31)  
- **Norman Door**: Bad design requiring labels due to conflicting affordances (pull handle vs. push door). (Slide 27)  

---

# Perception

## Overview
- **Perception**: experiences resulting from stimulation of the senses (sight, hearing, taste, smell, touch). (Slide 37)  
- Always a combination of **bottom-up** (sensory input) and **top-down** (knowledge, expectation) processing; best interpretation of stimulus. (Slide 39)  
  <!-- ![Perception demo](./perception_13.png) -->
- **Visual Dominance**: Visual sense often overrides other senses. (Slide 38)  

## Visual Perception
- **Eye anatomy**: light → retina → optic nerve → brain; lens adjusts focus (accommodation); fovea is high-resolution region. (Slide 38)  
- **Helmholtz’s Unconscious Inference**: Perception is the result of unconscious assumptions based on past experiences. we perceive what is most likely to have caused the stimuli via unconscious assumptions. (Slide 44)  
- **Illusions**: Examples include checker shadow (Slide 46), Ponzo (Slide 47), and ambiguous figures (Slide 44).  

## Gestalt Laws (Bottom-Up)
- **Proximity**: Elements close together are grouped. (Slide 53)  
- **Similarity**: Similar elements are grouped and assumed to share function. (Slide 54)  
- **Common Region**: Elements within the same closed region are grouped. (Slide 55)  
- **Continuity**: Elements aligned on a line or curve are perceived as related. (Slide 56)  
- **Closure**: We perceive complete figures even when part is missing. (Slide 57)  
- **Figure-Ground**: We distinguish objects (figure) from background. (Slide 58)  
- **Common Fate**: Elements moving together are grouped. (Slide 59)  
- **Design Application**: Used in UI (cards, navigation), logos, and animations. (Slides 53-59)  

## Dark (Deceptive) Patterns
- **Definition**: Design tricks leveraging cognition principles to induce actions not in users’ best interests. (Slide 62)  
- **Types**:  
  - Nagging: Persistent prompts with no opt-out (e.g., notification permissions). (Slide 65)  
  - Obstruction: Making unwanted actions hard (e.g., hidden unsubscribe links). (Slide 67)  
  - Sneaking: Hiding/delaying relevant info (e.g., disguised ads). (Slide 69)  
  - Interface Interference: Privileging certain actions (e.g., highlighting "keep driving"). (Slide 71)  
  - Forced Action: Requiring unrelated actions (e.g., signups for access). (Slide 64)  
- **XR Implications**: New deceptive patterns possible in augmented/virtual reality. (Slide 72)  

---

# Metaphors & Mental Models

## Definitions
- **Model**: Simplified description of a system or process. (Slide 78)  
- **Mental Model**: What the user believes about a system (belief-based, not facts). (Slide 78)  
- **Conceptual Model**: Designer’s high-level description of system organization. (Slide 78)  
- **Alignment Diagram**: Designer → Conceptual Model → System → Presented Model → User’s Mental Model. (Slide 76)  

## Mental Models in HCI
- **Alignment goal**: User’s mental model ↔ system’s conceptual & implemented models. (Slide 88)  
- **Levels**: From simple (child’s view) to advanced (expert’s view); use models "as simple as possible, as advanced as necessary". (Slide 83)  
- **Support**: Transparency, flexibility (accelerators), affordances, constraints, mappings. (Slide 89)  
- **Example**: Cloud storage mental models vary across generations (confusion about data location/sync). (Slide 87)  

## Transparency & Flexibility
- **Transparency**: Maintain external interface consistency despite internal changes (e.g., NFS vs FTP). (Slide 90)  
- **Flexibility**: Provide alternative task executions (e.g., copy-paste via mouse/shortcut; macros/gestures). (Slide 91)  

## Constraints
- **Physical**: Limit operations by shape/placement (e.g., connector shapes). (Slide 96)  
- **Logical**: Use reasoning to exclude solutions (e.g., valid calendar dates). (Slide 97)  
- **Semantic**: Leverage world knowledge (e.g., driver orientation in models). (Slide 98)  
- **Cultural**: Rely on conventions (e.g., red=stop); varies by culture (hand signs/color meanings). (Slide 99)  

## Mappings
- **Definition**: Relationship between controls and effects. (Slide 101)  
- **Types**:  
  - Spatial: Arrange controls like real objects (Slide 103)  
  - Physical: Mirror real-world behavior (e.g., rising water level = increase) (Slide 104)  
  - Cultural: Conform to conventions (e.g., left-to-right ordering) (Slide 105)  
  - Perceptual: Resemble controlled item (e.g., car seat controls) (Slide 106)  
- **Consistency**: Critical to avoid ambiguity (e.g., consistent softkey functions). (Slide 108)  

## Interface Metaphors
- **Purpose**: Exploit real-world knowledge to form mental models (e.g., desktop metaphor). (Slide 109)  
- **Noun-based**: Object properties transfer (e.g., folders). (Slide 111)  
- **Verb-based**: Action transfer (e.g., drag-and-drop). (Slide 112)  
- **Noun+Verb**: Combined (e.g., recycle bin). (Slide 113)  
- **Limits**: Can be restrictive, culturally biased, or hinder innovation (e.g., recycle bin inconsistencies). (Slides 114-115)  

## Errors & 7 Stages of Action
- **Mistakes**: Conscious errors from mental/conceptual model mismatch (e.g., cloud save confusion). (Slide 116)  
- **Slips**: Unconscious errors from inattention (e.g., misused hotkeys). (Slide 116)  
- **Seven Stages** (Norman):  
  1. Goal  
  2. Intention  
  3. Action Sequence  
  4. Execution  
  5. Perception  
  6. Interpretation  
  7. Evaluation  
  (Slides 119-123)  
- **Gulf of Execution**: Difficulty translating intentions into actions (mapping failure). (Slides 124-125)  
- **Gulf of Evaluation**: Difficulty interpreting feedback to assess goals. (Slides 126-127)  
- **Guidelines**: Address gulfs through perceivable functions, executable actions, clear feedback. (Slide 128)  