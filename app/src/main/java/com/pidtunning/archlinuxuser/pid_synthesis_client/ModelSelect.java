package com.pidtunning.archlinuxuser.pid_synthesis_client;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.Toast;

public class ModelSelect extends AppCompatActivity {

    private CheckBox fractional_model;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_model_select);

        // Define fractional checkbox
        fractional_model = (CheckBox) findViewById(R.id.checkBox_fractional_model);
        // Set fractional model by default
        fractional_model.setChecked(true);

        Button button_ingress_model = (Button) findViewById(R.id.button_ingress_model);
        button_ingress_model.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                openActivityIngressModel();
            }
        });
    }

    public void openActivityIngressModel(){
        // Open Activity with model list
        // If fractional model is checked then run that activity
        if ( this.fractional_model.isChecked() ) {
            Intent intent = new Intent(this, ModelIngress.class);
            startActivity(intent);
        } else {
            Toast.makeText(this,
                    getResources().getString(R.string.model_request_message),
                    Toast.LENGTH_SHORT).show();
        }
    }
}
