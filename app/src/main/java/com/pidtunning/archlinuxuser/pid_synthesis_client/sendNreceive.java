package com.pidtunning.archlinuxuser.pid_synthesis_client;

import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.support.annotation.Nullable;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;
import android.widget.Toast;
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.net.Socket;

public class sendNreceive extends AppCompatActivity {

    // Constants
    private static final int READ_REQUEST_CODE = 42;
    private static final int TIMEOUT = 30;
    private static final String SERVER_URL = "192.168.0.4";
    //private static final String SERVER_URL = "163.178.124.156";
    private static final int SERVER_PORT = 8494;
    private static final String MODEL_FILE_TYPE = "model_file";
    private static final String MODEL_FOTF_TYPE = "model_fotf";

    // Tunning results text view
    private static TextView textView_content;
    private volatile static String textView_cs_server_model_response;
    private volatile static String textView_cs_server_tunning_response;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_send_receive);

        textView_content = (TextView) findViewById(R.id.textTunningResults);

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
            searchTextFileAndSend();
        }
    }

    @Override
    protected void onStart (){
        super.onStart();

        // Refresh textview
        refresTextView();
    }

    private void refresTextView () {
        while (textView_cs_server_model_response == null) { }
        textView_content.setText(textView_cs_server_model_response);
        while (textView_cs_server_tunning_response == null) { }
        textView_content.setText(textView_cs_server_tunning_response);
    }

    private void sendModelRequest(final String model_type,
                                  final String model_data) {
        Thread thread = new Thread(new Runnable() {
            @Override
            public void run() {

                try {
                    //Replace below IP with the IP of that device in which server socket open.
                    //If you change port then change the port number in the server side code also.
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
         this.sendModelRequest(MODEL_FILE_TYPE, content.toString());
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
