package cloudschoolbus.guokrspace.com.creeperremote;

import android.os.Handler;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.util.Log;
import android.widget.EditText;
import android.widget.SeekBar;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import ninja.eigenein.joypad.JoypadView;
import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.Headers;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import okhttp3.ResponseBody;

public class MainActivity extends AppCompatActivity {

    String creeper_ip;
    OkHttpClient client;

    private static final int COMM_RIGHT = 0;
    private static final int COMM_FORWARD_RIGHT = 1;
    private static final int COMM_FORWARD = 2;
    private static final int COMM_FORWARD_LEFT = 3;
    private static final int COMM_LEFT = 4;
    private static final int COMM_BACKWARD = 5;
    private static final int COMM_BACKWARD_LEFT = 6;
    private static final int COMM_BACKWARD_RIGHT = 7;
    private static final int COMM_STOP = 8;

    Handler handler = new Handler(){
        public void handleMessage(android.os.Message msg) {
            sendMotorCommand(msg.what);
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);


         client = new OkHttpClient();


        final JoypadView joypadView = (JoypadView)findViewById(R.id.joypad_motor);
        joypadView.setListener(new JoypadView.Listener() {

            public void onUp() {
                handler.sendEmptyMessage(COMM_STOP);
            }

            public void onMove(float distance, float dx, float dy) {
                if (distance < 0.20) {
                    return;
                }

                if (distance < 0.33) {

                } else if (distance < 0.66) {

                } else if (distance < 1) {

                }

                double degree = getAngle(dx, dy); // Y Axis Position Clockwise(0 - 180) CouterClockwise(0 - -180)

                //Right
                if (degree < 22.5 && degree >= -22.5) {
                    handler.sendEmptyMessage(COMM_RIGHT);
                }
                //Fowrad Right
                else if (degree >= 22.5 && degree < 67.5) {
                    handler.sendEmptyMessage(COMM_FORWARD_RIGHT);
                }
                //Forward
                else if (degree >= 67.5 && degree < 112.5) {
                    handler.sendEmptyMessage(COMM_FORWARD);
                }
                //Forward Left
                else if (degree >= 112.5 && degree < 157.5) {
                    handler.sendEmptyMessage(COMM_FORWARD_LEFT);
                }
                //LEFT
                else if ((degree > 157.5 && degree <= 180) || (degree < -157.5 && degree >= -180)) {
                    handler.sendEmptyMessage(COMM_LEFT);
                }
                // Backward Left
                else if (degree >= -157.5 && degree < -112.5)
                {
                    handler.sendEmptyMessage(COMM_BACKWARD_LEFT);
                }
                else if (degree >= -112.5 && degree < -67.5) {
                    handler.sendEmptyMessage(COMM_BACKWARD);
                //Backward Right
                } else if (degree >= -67.5 && degree < -22.5) {
                    handler.sendEmptyMessage(COMM_BACKWARD_RIGHT);
                } else {
                    handler.sendEmptyMessage(COMM_STOP);
                }

            }
        });

        /*SeekBar seekBarLeft = (SeekBar)findViewById(R.id.seekBarLeft);

        seekBarLeft.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int i, boolean b) {
                Log.i("", Integer.toString(i));
                power_level = ((float)(i-50)*2)/100;
                handler.sendEmptyMessage(0);
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {

            }
        });

        SeekBar seekBarRight = (SeekBar)findViewById(R.id.seekBarRight);

        seekBarRight.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int i, boolean b) {
                Log.i("", Integer.toString(i));
                power_level = (float)(i-50)*2/100;
                handler.sendEmptyMessage(1);
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {

            }
        });*/


        EditText ipaddressEditText = (EditText)findViewById(R.id.edittext_ipaddress);
        ipaddressEditText.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence charSequence, int i, int i1, int i2) {

            }

            @Override
            public void onTextChanged(CharSequence charSequence, int i, int i1, int i2) {

            }

            @Override
            public void afterTextChanged(Editable editable) {
                creeper_ip = editable.toString();

                Log.i("", creeper_ip);
            }
        });

    }

    public static double getAngle(float x, float y)
    {
        return (180/Math.PI * Math.atan2(y,x)); //note the atan2 call, the order of paramers is y then x
    }

    private void sendMotorCommand(int direction)
    {
        final List<String> urls = new ArrayList(){};
        switch (direction)
        {
            case COMM_FORWARD: //Forward
                urls.add("http://" + creeper_ip + "/powerleft/" + String.valueOf(0.8));
                urls.add("http://" + creeper_ip + "/powerright/" + String.valueOf(0.8));
                break;
            case COMM_BACKWARD: //Backward
                urls.add("http://" + creeper_ip + "/powerleft/" + String.valueOf(-0.8));
                urls.add("http://" + creeper_ip + "/powerright/" + String.valueOf(-0.8));
                break;
            case COMM_LEFT: //Left
                urls.add("http://" + creeper_ip + "/powerleft/" + String.valueOf(-0.4));
                urls.add("http://" + creeper_ip + "/powerright/" + String.valueOf(0.8));
                break;
            case COMM_RIGHT: //Right
                urls.add("http://" + creeper_ip + "/powerleft/" + String.valueOf(0.8));
                urls.add("http://" + creeper_ip + "/powerright/" + String.valueOf(-0.4));
                break;
            case COMM_FORWARD_RIGHT: //Forward-Right
                urls.add("http://" + creeper_ip + "/powerleft/" + String.valueOf(0.3));
                urls.add("http://" + creeper_ip + "/powerright/" + String.valueOf(1));
                break;
            case COMM_BACKWARD_RIGHT: //Backward-Right
                urls.add("http://" + creeper_ip + "/powerleft/" + String.valueOf(-1));
                urls.add("http://" + creeper_ip + "/powerright/" + String.valueOf(-0.3));
                break;
            case COMM_BACKWARD_LEFT: //Backward-Left
                urls.add("http://" + creeper_ip + "/powerleft/" + String.valueOf(-0.3));
                urls.add("http://" + creeper_ip + "/powerright/" + String.valueOf(-1));
                break;
            case COMM_FORWARD_LEFT: //Forward-Left
                urls.add("http://" + creeper_ip + "/powerleft/" + String.valueOf(0.3));
                urls.add("http://" + creeper_ip + "/powerright/" + String.valueOf(1));
                break;
            default: //Brake
                if(creeper_ip!=null && creeper_ip!="") {
                    urls.add("http://" + creeper_ip + "/brake/");
                }
                break;
        }

        Thread thread = new Thread(new Runnable() {
            @Override
            public void run() {
                for(String url : urls) {
                    Request request = new Request.Builder().url(url).build();
                    client.newCall(request).enqueue(new okhttp3.Callback() {
                        @Override
                        public void onFailure(Call call, IOException e) {
                            e.printStackTrace();
                        }

                        @Override
                        public void onResponse(Call call, Response response) throws IOException {
                            if (!response.isSuccessful())
                                throw new IOException("Unexpected code " + response);
                            Headers responseHeaders = response.headers();
                            for (int i = 0; i < responseHeaders.size(); i++) {
                                System.out.println(responseHeaders.name(i) + ": " + responseHeaders.value(i));
                            }
                            System.out.println(response.body().string());
                        }
                    });
                }
            }
        });
        thread.start();
    }
}