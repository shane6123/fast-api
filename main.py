from mangum import Mangum
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware  # Import the CORSMiddleware
import rembg
from PIL import Image
import io

app = FastAPI()

# Allow all origins for simplicity. Adjust it based on your needs.
origins = ["*"]

# Use the CORSMiddleware with your FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/fastapi")
async def read_fastapi():
    return {"Hello": "FastAPI"}

@app.post("/remove-image-bg")
async def remove_image_bg(image: UploadFile = File(...)):
    try:
        if not image:
            raise HTTPException(status_code=400, detail="No file provided")
        image_data = await image.read()

        # Remove background using rembg library
        output_data = rembg.remove(image_data)

        # Create a PIL Image from the output data
        output_image = Image.open(io.BytesIO(output_data))

        # Save the output image (optional)
        # output_image.save('output.png')

        # Send the image as a response
        output_buffer = io.BytesIO()
        output_image.save(output_buffer, format='PNG')
        output_buffer.seek(0)

        return StreamingResponse(io.BytesIO(output_buffer.read()), media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Wrap the existing code with the Mangum handler
handler = Mangum(app)
