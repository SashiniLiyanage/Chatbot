## Build & Use

1. Create a virtual environment
 
2. Install the required dependencies by running the following command:
   ```
   pip install -r requirements.txt
   ```

3. OpenAI API key to the `.env` file and specify the folder path to upload pdfs (use the same name given below)
   ```
   OPENAI_API_KEY=your_secrit_api_key
   UPLOAD_FOLDER = 'pdf_uploads'
   ```

4. Run the following command to build the app
   ```
   python app.py
   ```

5. Load multiple PDF documents into the app and press "PROCESS" button