package com.example.newcropsol;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.media.ThumbnailUtils;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.view.View;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import com.example.newcropsol.ml.FinalCheckimg;
import com.example.newcropsol.ml.FinalcropsolmodelNew;

import org.tensorflow.lite.DataType;
import org.tensorflow.lite.support.tensorbuffer.TensorBuffer;

import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;

public class Camera extends AppCompatActivity {

    TextView result, clickHere, capturetext, classified, invalidtext, displayMsg;
    ImageView imageView;
    Button camera, gallery;

    int imageSize = 256; //default image size

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getSupportActionBar().hide();
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);
        setContentView(R.layout.activity_camera);

        camera = findViewById(R.id.camera);
        gallery = findViewById(R.id.gallery);
        clickHere = findViewById(R.id.clickHere);
        result = findViewById(R.id.result);
        imageView = findViewById(R.id.imageView);
        capturetext = findViewById(R.id.capturetext);
        classified = findViewById(R.id.classified);
        invalidtext = findViewById(R.id.invalidtext);
        displayMsg = findViewById(R.id.displayMsg);

        capturetext.setVisibility(View.VISIBLE);
        displayMsg.setVisibility(View.GONE);
        invalidtext.setVisibility(View.GONE);
        classified.setVisibility(View.GONE);
        clickHere.setVisibility(View.GONE);

        camera.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                //launch camera if we have permission
                if (checkSelfPermission(Manifest.permission.CAMERA) == PackageManager.PERMISSION_GRANTED) {
                    Intent cameraIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
                    startActivityForResult(cameraIntent, 3);
                } else {
                    //request camera permission if we don't have
                    requestPermissions(new String[]{Manifest.permission.CAMERA}, 100);
                }
            }
        });

        gallery.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent cameraIntent = new Intent(Intent.ACTION_PICK, MediaStore.Images.Media.EXTERNAL_CONTENT_URI);
                startActivityForResult(cameraIntent, 1);
            }
        });
    }

    private void classifyImage(Bitmap image) {
        try {
            FinalcropsolmodelNew model = FinalcropsolmodelNew.newInstance(getApplicationContext());

            // Creates inputs for reference.
            TensorBuffer inputFeature0 = TensorBuffer.createFixedSize(new int[]{1, 256, 256, 3}, DataType.FLOAT32);
            ByteBuffer byteBuffer = ByteBuffer.allocateDirect(4 * imageSize * imageSize * 3);
            byteBuffer.order(ByteOrder.nativeOrder());

            int[] intValues = new int[imageSize * imageSize];
            image.getPixels(intValues, 0, image.getWidth(), 0, 0, image.getWidth(), image.getHeight());

            int pixel = 0;

            for (int i = 0; i < imageSize; i++) {
                for (int j = 0; j < imageSize; j++) {
                    int val = intValues[pixel++]; //RGB
                    byteBuffer.putFloat(((val >> 16) & 0xFF) * (1.f / 1));
                    byteBuffer.putFloat(((val >> 8) & 0xFF) * (1.f / 1));
                    byteBuffer.putFloat((val & 0xFF) * (1.f / 1));
                }
            }
            inputFeature0.loadBuffer(byteBuffer);

            // Runs model inference and gets result.
            FinalcropsolmodelNew.Outputs outputs = model.process(inputFeature0);
            TensorBuffer outputFeature0 = outputs.getOutputFeature0AsTensorBuffer();

            float[] confidence = outputFeature0.getFloatArray();
            //find the index of the class with the biggest confidence
            int maxPos = 0;
            float maxConfidence = 0;
            for (int i = 0; i < confidence.length; i++) {
                if (confidence[i] > maxConfidence) {
                    maxConfidence = confidence[i];
                    maxPos = i;
                }
            }

            String[] classes = {"Curry Leaves","Healthy Brinjal Leaf","Healthy Cassava Leaf","Healthy Centella asiatica (Gotu kola)",
                    "Lemon Leaf","Malabar spinach Leaf (Nivithi)","Potato Double Round Pattern Bottle disease",
                    "Red pepper Bacterial spot disease","Tomato Bacterial spot disease","Winged Bean leaf"};
            result.setText(classes[maxPos]);

            clickHere.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    //search in Google
                    startActivity(new Intent(Intent.ACTION_VIEW,
                            Uri.parse("https://www.google.com/search?q=" + result.getText())));
                }
            });

            // Releases model resources if no longer used.
            model.close();
        } catch (IOException e) {
            // TODO Handle the exception
        }
    }

    private int classifyImage2(Bitmap image) {
        try {
            FinalCheckimg model = FinalCheckimg.newInstance(getApplicationContext());

            // Creates inputs for reference.
            TensorBuffer inputFeature0 = TensorBuffer.createFixedSize(new int[]{1, 256, 256, 3}, DataType.FLOAT32);
            ByteBuffer byteBuffer = ByteBuffer.allocateDirect(4 * imageSize * imageSize * 3);
            byteBuffer.order(ByteOrder.nativeOrder());

            int[] intValues = new int[imageSize * imageSize];
            image.getPixels(intValues, 0, image.getWidth(), 0, 0, image.getWidth(), image.getHeight());

            int pixel = 0;

            for (int i = 0; i < imageSize; i++) {
                for (int j = 0; j < imageSize; j++) {
                    int val = intValues[pixel++]; //RGB
                    byteBuffer.putFloat(((val >> 16) & 0xFF) * (1.f / 1));
                    byteBuffer.putFloat(((val >> 8) & 0xFF) * (1.f / 1));
                    byteBuffer.putFloat((val & 0xFF) * (1.f / 1));
                }
            }
            inputFeature0.loadBuffer(byteBuffer);

            // Runs model inference and gets result.
            FinalCheckimg.Outputs outputs = model.process(inputFeature0);
            TensorBuffer outputFeature0 = outputs.getOutputFeature0AsTensorBuffer();

            float[] confidence = outputFeature0.getFloatArray();
            //find the index of the class with the biggest confidence
            int maxPos = 0;
            float maxConfidence = 0;
            for (int i = 0; i < confidence.length; i++) {
                if (confidence[i] > maxConfidence) {
                    maxConfidence = confidence[i];
                    maxPos = i;
                }
            }

            String[] classes = {"Invalid Image", "Valid Image"};
            model.close();
            if (maxPos == 0) {
                result.setText(classes[maxPos]);
                clickHere.setVisibility(View.GONE);
                classified.setVisibility(View.GONE);
                invalidtext.setVisibility(View.VISIBLE);
                displayMsg.setVisibility(View.VISIBLE);
            }
            return maxPos;

        } catch (IOException e) {
            return 3;
            // TODO Handle the exception
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        if (resultCode == RESULT_OK) {
            if (requestCode == 3) {
                Bitmap image = (Bitmap) data.getExtras().get("data");
                int dimension = Math.min(image.getWidth(), image.getHeight());
                image = ThumbnailUtils.extractThumbnail(image, dimension, dimension);
                imageView.setImageBitmap(image);

                capturetext.setVisibility(View.GONE);
                invalidtext.setVisibility(View.GONE);
                displayMsg.setVisibility(View.GONE);
                classified.setVisibility(View.VISIBLE);
                clickHere.setVisibility(View.VISIBLE);

                image = Bitmap.createScaledBitmap(image, imageSize, imageSize, false);
                //classifyImage(image);
                if (classifyImage2(image) == 1) {
                    classifyImage(image);
                }

            } else {
                Uri dat = data.getData();
                Bitmap image = null;
                try {
                    image = MediaStore.Images.Media.getBitmap(this.getContentResolver(), dat);
                } catch (IOException e) {
                    e.printStackTrace();
                }
                imageView.setImageBitmap(image);

                capturetext.setVisibility(View.GONE);
                invalidtext.setVisibility(View.GONE);
                displayMsg.setVisibility(View.GONE);
                classified.setVisibility(View.VISIBLE);
                clickHere.setVisibility(View.VISIBLE);

                image = Bitmap.createScaledBitmap(image, imageSize, imageSize, false);
                //classifyImage(image);
                if (classifyImage2(image) == 1) {
                    classifyImage(image);
                }
            }
        }
        super.onActivityResult(requestCode, resultCode, data);
    }
}