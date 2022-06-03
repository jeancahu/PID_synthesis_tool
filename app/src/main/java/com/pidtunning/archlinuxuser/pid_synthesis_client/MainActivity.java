package com.pidtunning.archlinuxuser.pid_synthesis_client;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Build;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.Toast;


public class MainActivity extends AppCompatActivity {

    // Constants
    private static final int PERMISSION_REQUEST_STORAGE = 1000;

    private CheckBox checkBox_PID;
    private CheckBox checkBox_PI;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Define buttons
        Button button_model = (Button) findViewById(R.id.button_model);
        Button button_file = (Button) findViewById(R.id.button_file);

        //Define checkboxs
        checkBox_PI = (CheckBox) findViewById(R.id.checkBox_PI);
        checkBox_PID = (CheckBox) findViewById(R.id.checkBox_PID);

        // Select PI by default
        checkBox_PI.setChecked(true);

        button_model.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                openActivityModelSelect();
            }
        });
        button_file.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // Search the file from external storage
                openActivitySendReceive();
            }
        });

        checkBox_PI.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                checkbox_PI_checked_verif();
            }
        });
        checkBox_PID.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                checkbox_PID_checked_verif();
            }
        });

        // Request permission
        if(Build.VERSION.SDK_INT >= Build.VERSION_CODES.M &&
                checkSelfPermission(Manifest.permission.WRITE_EXTERNAL_STORAGE)
                        != PackageManager.PERMISSION_GRANTED){
            requestPermissions(new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE},
                    PERMISSION_REQUEST_STORAGE);
        }
    }

    private void checkbox_PI_checked_verif (){
        if (this.checkBox_PI.isChecked() ){
            this.checkBox_PID.setChecked(false);
        }
    }
    private void checkbox_PID_checked_verif (){
        if (this.checkBox_PID.isChecked() ){
            this.checkBox_PI.setChecked(false);
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode,
                                           @NonNull String[] permissions,
                                           @NonNull int[] grantResults) {
        // Consulting storage read permission
        if(requestCode == PERMISSION_REQUEST_STORAGE){
            if (grantResults[0] == PackageManager.PERMISSION_GRANTED){
                Toast.makeText(this,
                        getResources().getString(R.string.permitted_info_message),
                        Toast.LENGTH_SHORT).show();
            } else {
                Toast.makeText(this,
                        getResources().getString(R.string.denied_info_message),
                        Toast.LENGTH_SHORT).show();
            }
        }
    }

    public void openActivityModelSelect(){
        // Go to next activity, select model and params
        Intent intent = new Intent(this, ModelSelect.class);
        startActivity(intent);
    }

    public void openActivitySendReceive(){
        // Request permission
        if(Build.VERSION.SDK_INT >= Build.VERSION_CODES.M &&
                checkSelfPermission(Manifest.permission.READ_EXTERNAL_STORAGE)
                        != PackageManager.PERMISSION_GRANTED){
            requestPermissions(new String[]{Manifest.permission.READ_EXTERNAL_STORAGE},
                    PERMISSION_REQUEST_STORAGE);
        } else {
            // Go to next activity, send and receive params
            Intent intent = new Intent(this, sendNreceive.class);
            startActivity(intent);
        }
    }
}
