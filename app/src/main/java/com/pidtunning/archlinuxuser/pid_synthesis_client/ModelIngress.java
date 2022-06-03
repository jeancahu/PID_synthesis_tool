package com.pidtunning.archlinuxuser.pid_synthesis_client;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

public class ModelIngress extends AppCompatActivity {

    private EditText editText_v;
    private EditText editText_T;
    private EditText editText_kp;
    private EditText editText_L;

    private Button continueTunning;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_model_ingress);
        editText_v = (EditText) findViewById(R.id.editText_v);
        editText_T = (EditText) findViewById(R.id.editText_T);
        editText_kp = (EditText) findViewById(R.id.editText_K);
        editText_L = (EditText) findViewById(R.id.editText_L);

        continueTunning = (Button) findViewById(R.id.button_synth);

        continueTunning.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if ( verifyValues() ) {
                    openActivitySendReceive();
                }
            }
        });
    }

    private boolean verifyValues(){
        // Verify range and values
        if ( Float.parseFloat(editText_v.getText().toString()) < 1.0
                || Float.parseFloat(editText_v.getText().toString()) > 1.8){
            Toast.makeText(this,
                    getResources().getString(R.string.frac_const_value_request_message),
                    Toast.LENGTH_SHORT).show();
            return false;
        }
        // TODO: Verify the others values
        return true;
    }

    private void openActivitySendReceive (){
        // Notify state
        Toast.makeText(this,
                getResources().getString(R.string.processing_info_message),
                Toast.LENGTH_SHORT).show();
        // Go to next activity, send and receive params
        Intent intent = new Intent(this, sendNreceive.class);
        intent.putExtra("v_value", editText_v.getText().toString());
        intent.putExtra("T_value", editText_T.getText().toString());
        intent.putExtra("kp_value", editText_kp.getText().toString());
        intent.putExtra("L_value", editText_L.getText().toString());
        startActivity(intent);
    }

}
