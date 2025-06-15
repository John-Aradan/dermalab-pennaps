# ML-Powered Medical Diagnostic Insights

Dermalab -  Your trusted partner for skin diagnosis, leveraging AI, ML, deep learning, and LLMs for precise evaluations, comprehensive insights, and compelling doctor-patient relationships. 

Dermalab helps avoid in skin disease misdiagosis via real-time skin condition classification, disease severity calculation, and spread predictions using cutting-edge technology. We've consolidated all of our amazing features on a website that anybody can use!


# Usage

## Disease Classification
Users first have an option of uploading pictures of the affected area to the website. Our machine learning algorithm will then classify and identify the disease or condition that is present, if any. Instead of outputting just one condition from an input, dermalab outputs several ranked diseases that doctors can further interpret based upon a patients individuality

### LLMs for Simplifying Medical Jargon
However, we don't stop there! Users also receive a summary of their conditions - without all of the hard-to-understand medical jargon. That way, both patients and doctors are on the same page when it comes to understanding a disease diagnosis. We used [Metaphor's API](https://platform.metaphor.systems/) and [Replicate](https://replicate.com/) to do this. 

## Severity Calculation
Our web page also gives users the choice of completing a questionnaire to return the severity level of the disease. We provide explanations for each severity level to ensure that this process is empathetic to patients in the best way possible. 

## Spread Breakdown
Our deep learning algorithm outputs the predicted disease spread for doctors as well. This was done via further analysis through deep learning and MATLAB to understand region, rate, and direction of disease growth. We used the InceptionResNetV2 model, with lesion images and their annotated masks to train the deep learning model, to perform semantic segmentation on unseen data. Once the semantic segmentation of lesions are done, thereby performing binary masks, MATLAB could be used to perform an onion ring segmentation of the region, where dilation and erosion of mask is done and the difference is taken.

Combined, the variety of services that dermalab provides a robust interface for doctors and patients during disease diagnoses, and helps prevents misdiagnoses.

