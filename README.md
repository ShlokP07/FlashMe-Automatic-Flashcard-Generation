# FlashMe-Automatic-Flashcard-Generation

![logo-no-background1](https://github.com/ShlokP07/FlashMe-Automatic-Flashcard-Generation/assets/22417910/838bc5ef-93b8-4b0d-ac45-4d348e556935)

## Table of Contents
* [About the project](#about-the-project)
* [Installation](#installation)
* [Diagrams](#diagrams)
* [Technology Used](#technology-used)
* [Authors](#authors)
* [Credits](#credits)
* [Refrences](#refrences)


## About the project

The most effective way to learn is through the use of flashcards due to their high interactivity and reliance on active recall. The key to creating effective flashcards is generating the correct question-answer pairs. For this, one needs to deploy question generation and answer extraction models that are both light and accurate. Extracting possible answers from a text is done based on keywords. Identifying those keywords to extract possible answers and generate questions based on them is not a simple procedure. Handling all these tasks and delivering accurate results cannot be done effectively by a single model. Therefore the proposed system contains a pipeline of 4 modules viz., text summarization, answer extraction, question generation, and filtering.

Summarization is used to condense technically dense input into lucid text. It helps improve inference down the pipeline. The proposed system uses a DistilBART model to generate abstractive summarization. The model will be fed with an input of 1024 tokens. The output will be a summary of the text of variable length.

A combined dataset of SQuAD, RACE, and COQA was used for answer extraction, as this makes the model more robust and improves its performance with textbook data. Following cleansing and concatenation, the final dataset contained approximately 200,000 examples. Input to the model will be the highlighted sentence and the rest of the paragraph (for additional context). The input paragraph is clipped to 512 tokens to match the maximum input size. Output from the model, i.e., answer aware texts, will be fed to the question generation model.  Questions will be generated with a similar T5 model.

Some of the generated questions will be redundant, so they must be filtered out. The proposed system uses similarity measures to do this effectively. Generated questions along with their corresponding paragraphs will be fed to a DistilBert model. The answer extracted in the second step will be compared with Distilbert's output. Low similarity questions are discarded.

Thus, by utilizing our technology's ability to generate flashcards from study material, students can save valuable time that would otherwise be spent taking traditional notes. This additional time can be used by students to participate in extracurricular activities, which can enhance their overall academic experience and personal growth.

Furthermore, the interactive nature of flashcards is highly beneficial for engaging students in the learning process. Through active recall, students can improve their ability to retain information from the syllabi they have studied. By repeatedly practicing with flashcards, students can develop a stronger understanding of the course material, which can lead to better academic performance.

## Installation
To install all necessary dependencies, run the following command in the terminal:
pip install -r requirements.txt

## Diagrams
### **Architecture**
![BlockDiagram_new](https://github.com/ShlokP07/FlashMe-Automatic-Flashcard-Generation/assets/22417910/450c2cf7-04bc-4567-ad52-781902ec0b6d)

### **Activity**
![Activitydiagram_new](https://github.com/ShlokP07/FlashMe-Automatic-Flashcard-Generation/assets/22417910/2e1d2d5a-db9b-4c98-9f67-bccd64d44184)

## Technology Used

## Authors

## Credits

