package com.pidtunning.archlinuxuser.pid_synthesis_client;

import android.app.Activity;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.RectF;
import android.graphics.Typeface;
import android.net.Uri;
import android.os.Environment;
import android.provider.MediaStore;
import android.renderscript.Element;
import android.support.annotation.Nullable;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.BoringLayout;
import android.util.Base64;
import android.util.Base64InputStream;
import android.view.View;
import android.widget.CheckBox;
import android.widget.CompoundButton;
import android.widget.ImageView;
import android.widget.ProgressBar;
import android.widget.Switch;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.ToggleButton;

import com.github.chrisbanes.photoview.PhotoView;

import java.io.BufferedReader;
import java.io.ByteArrayInputStream;
import java.io.DataInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.Map;
import java.util.TreeMap;

public class sendNreceive extends AppCompatActivity {

    // Constants
    private static final int READ_REQUEST_CODE = 42;
    private static final int TIMEOUT = 30;

    //private static final String SERVER_URL = "192.168.0.4";
    private static final String SERVER_URL = "163.178.124.156";

    private static final int SERVER_PORT = 8494;
    private static final String MODEL_FILE_TYPE = "model_file";
    private static final String MODEL_FOTF_TYPE = "model_fotf";

    private static Map<String, Bitmap> images = new TreeMap<String, Bitmap>();

    // Tunning results text view
    private static TextView textView_content;
    // private static ImageView imageView_content;
    private static PhotoView imageView_content;
    private static Bitmap image_result;
    private static ToggleButton showImage;
    private static ProgressBar receive_bar;

    private static CheckBox PI_14;
    private static CheckBox PI_20;
    private static CheckBox PID_14;
    private static CheckBox PID_20;


    //private volatile static Boolean response_verified;
    private volatile static String textView_cs_server_model_response;
    private volatile static String textView_cs_server_tunning_response;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_send_receive);

        //this.response_verified = Boolean.FALSE;
        textView_content = (TextView) findViewById(R.id.textTunningResults);
        textView_content.setTypeface(Typeface.MONOSPACE);

        imageView_content = (PhotoView) findViewById(R.id.simulation_view);
        showImage = (ToggleButton) findViewById(R.id.showImage);

        receive_bar = (ProgressBar) findViewById(R.id.recepcion);

        PI_14 = (CheckBox) findViewById(R.id.PI_14);
        PI_20 = (CheckBox) findViewById(R.id.PI_20);
        PID_14 = (CheckBox) findViewById(R.id.PID_14);
        PID_20 = (CheckBox) findViewById(R.id.PID_20);

        showImage.setVisibility(View.GONE);
        imageView_content.setVisibility(View.GONE);
        PID_14.setVisibility(View.GONE);
        PID_20.setVisibility(View.GONE);
        PI_14.setVisibility(View.GONE);
        PI_20.setVisibility(View.GONE);

        PID_20.setChecked(Boolean.TRUE);
        PID_14.setChecked(Boolean.TRUE);
        PI_20.setChecked(Boolean.TRUE);
        PI_14.setChecked(Boolean.TRUE);

        receive_bar.setMax(20);
        receive_bar.setProgress(3);

        String params;
        Bundle bundle = getIntent().getExtras();
        if (bundle != null) {
            params = bundle.getString("v_value")+',';
            params += bundle.getString("T_value")+',';
            params += bundle.getString("kp_value")+',';
            params += bundle.getString("L_value");
            this.sendModelRequest(MODEL_FOTF_TYPE, params);
        } else {
            // Search for a response file
            textView_cs_server_tunning_response = "No data";
            this.searchTextFileAndSend();
        }

        showImage.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if (isChecked) {
                    textView_content.setVisibility(View.GONE);
                    imageView_content.setVisibility(View.VISIBLE);
                    PID_14.setVisibility(View.VISIBLE);
                    PID_20.setVisibility(View.VISIBLE);
                    PI_14.setVisibility(View.VISIBLE);
                    PI_20.setVisibility(View.VISIBLE);

                    PI_20.setChecked(Boolean.FALSE);
                    PI_14.setChecked(Boolean.FALSE);
                    PI_20.setEnabled(Boolean.FALSE);
                    PI_14.setEnabled(Boolean.FALSE);

                    PID_20.setChecked(Boolean.FALSE);
                    PID_14.setChecked(Boolean.FALSE);
                    PID_20.setEnabled(Boolean.FALSE);
                    PID_14.setEnabled(Boolean.FALSE);

                    if(images.containsKey("ARD")) {
                        PI_14.setEnabled(Boolean.TRUE);
                        PI_14.setChecked(Boolean.TRUE);
                    }
                    if(images.containsKey("BRD")) {
                        PI_20.setEnabled(Boolean.TRUE);
                        PI_20.setChecked(Boolean.TRUE);
                    }
                    if(images.containsKey("CRD")) {
                        PID_14.setEnabled(Boolean.TRUE);
                        PID_14.setChecked(Boolean.TRUE);
                    }
                    if(images.containsKey("DRD")) {
                        PID_20.setEnabled(Boolean.TRUE);
                        PID_20.setChecked(Boolean.TRUE);
                    }

                    setImageToShow();
                } else {
                    textView_content.setVisibility(View.VISIBLE);
                    imageView_content.setVisibility(View.GONE);
                    PID_14.setVisibility(View.GONE);
                    PID_20.setVisibility(View.GONE);
                    PI_14.setVisibility(View.GONE);
                    PI_20.setVisibility(View.GONE);
                }
            }
        });

        PI_14.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                setImageToShow();
            }
        });
        PI_20.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                setImageToShow();
            }
        });
        PID_14.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                setImageToShow();
            }
        });
        PID_20.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                setImageToShow();
            }
        });
    }

    private void setImageToShow (){
        String image_name = "";
        if(PI_14.isChecked()){
            image_name += "A";
        }
        if(PI_20.isChecked()){
            image_name += "B";
        }
        if(PID_14.isChecked()){
            image_name += "C";
        }
        if(PID_20.isChecked()){
            image_name += "D";
        }
        image_name += "RD";

        // TODO: Keep zoom and position
        imageView_content.setImageBitmap(images.get(image_name));
    }

    private void sendModelRequest(final String model_type,
                                  final String model_data) {
        Thread thread = new Thread(new Runnable() {
            @Override
            public void run() {

                try {
                    //Replace below IP with the IP of that device in which server socket open.
                    //If you change port then change the port number in the server side code also.

                    //response_verified = Boolean.FALSE;

                    Socket s = new Socket(SERVER_URL, SERVER_PORT);

                    InputStream in = s.getInputStream();
                    InputStreamReader sr_input = new InputStreamReader(
                            in, "UTF-8");
                    BufferedReader input = new BufferedReader(sr_input);

                    OutputStream out = s.getOutputStream();
                    PrintWriter output = new PrintWriter(out);

                    // Send the model type
                    output.println(model_type);
                    output.flush();

                    // Receive confirmation
                    String model_server_response = "";
                    String temporal = "";
                    do {
                        model_server_response += temporal;
                        temporal = input.readLine();
                    } while ( ! temporal.contains("EOF") ); // Search for EOF
                    //input.reset();
                    textView_cs_server_model_response = model_server_response;

                    // Send the model data
                    output.println(model_data+"\nEOF\n");
                    output.flush();

                    // Receive tunning results and show
                    // Receive confirmation
                    String tunning_results = "";
                    temporal = "";
                    do {
                        tunning_results += temporal;
                        temporal = input.readLine()+'\n';
                    } while ( ! temporal.contains("EOF") ); // Search for EOF

                    // Refresh tunning results
                    textView_cs_server_tunning_response = tunning_results;

                    // Refresh controllers table
                    runOnUiThread(new Runnable(){
                        @Override
                        public void run(){
                            textView_content.setText(textView_cs_server_tunning_response);
                        }
                    });

                    // Receive image name
                    temporal = input.readLine();
                    //input.close();

                    // Clear images map
                    images.clear();

                    // Load raw data from server
                    DataInputStream dataInputStream = new DataInputStream(in);

                    do {

                        // Send receive message
                        output.println("ImageNameReceived");
                        output.flush();

                        image_result = BitmapFactory.decodeStream(dataInputStream);
                        //dataInputStream.close();
                        images.put(temporal, image_result);

                        // Send receive message
                        //output.println("ImageReceived");
                        //output.flush();

                        temporal = input.readLine();

                        runOnUiThread(new Runnable(){
                            @Override
                            public void run(){
                                receive_bar.setProgress(receive_bar.getProgress()+1);
                            }
                        });

                    } while ( ! temporal.contains("END") ); // Search end of array

                    // Enable Switch
                    runOnUiThread(new Runnable(){
                        @Override
                        public void run(){
                            showImage.setVisibility(View.VISIBLE);
                            receive_bar.setProgress(receive_bar.getMax());
                        }
                    });

                    output.close();
                    out.close();
                    s.close();
                } catch (IOException e) {
                    e.printStackTrace();

                }
            }
        });

        thread.start();
    }

    // Read content from a file path, set this.file_content
    private void setResponseFileContent (Uri uri) {
        // File content
        StringBuilder content = new StringBuilder();
        try {
            InputStream inputStream = getContentResolver().openInputStream(uri);
            BufferedReader reader = new BufferedReader(
                new InputStreamReader(inputStream));
            String line;
            while (( line = reader.readLine()) != null ){
                content.append(line);
                content.append('\n');
            }
            inputStream.close();
        } catch (FileNotFoundException e) {
            Toast.makeText(this,
                    getResources().getString(R.string.file_not_found_err_message),
                    Toast.LENGTH_SHORT).show();
            e.printStackTrace();
        } catch (IOException e) {
            Toast.makeText(this,
                    getResources().getString(R.string.file_permission_err_message),
                    Toast.LENGTH_SHORT).show();
            e.printStackTrace();
        }
        Toast.makeText(this,
                getResources().getString(R.string.file_sending_info_message),
                Toast.LENGTH_SHORT).show();
        this.sendModelRequest(MODEL_FILE_TYPE, content.toString());

        // Show data array
        textView_content.setText(content.toString());
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        if (requestCode == READ_REQUEST_CODE && resultCode == Activity.RESULT_OK){
            // Set file response content
            if (data != null){
                Uri uri = data.getData();
                Toast.makeText(this,
                        getResources().getString(R.string.file_reading_info_message),
                        Toast.LENGTH_SHORT).show();
                setResponseFileContent(uri);
            }
        }
    }

    public void searchTextFileAndSend(){
        // Open Activity with model list
        Intent intent = new Intent(Intent.ACTION_GET_CONTENT);
        intent.addCategory(Intent.CATEGORY_OPENABLE);
        // Select all possible text types
        intent.setType("text/*");
        startActivityForResult(intent, READ_REQUEST_CODE);
    }
}
