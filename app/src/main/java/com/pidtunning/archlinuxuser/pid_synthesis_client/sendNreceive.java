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

public class sendNreceive extends AppCompatActivity {

    // Constants
    private static final int READ_REQUEST_CODE = 42;

    private static String file_content; // Response file content
    TextView textView_content;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_send_receive);

        // Search for a response file
        searchTextFile();

        // Show content preview
        textView_content = (TextView) findViewById(R.id.textFileContent);
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
         this.file_content = content.toString();
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

    public void searchTextFile(){
        // Open Activity with model list
        Intent intent = new Intent(Intent.ACTION_GET_CONTENT);
        intent.addCategory(Intent.CATEGORY_OPENABLE);
        // Select all possible text types
        intent.setType("text/*");
        startActivityForResult(intent, READ_REQUEST_CODE);
    }
}
