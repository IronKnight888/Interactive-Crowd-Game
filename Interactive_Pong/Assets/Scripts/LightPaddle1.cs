using UnityEngine;

public class LightPaddle1 : Paddle
{
    UDPSocket inputData;
    public float y;

    private void Awake()
    {
        rb = GetComponent<Rigidbody2D>();
        inputData = GameObject.Find("Input Data").GetComponent<UDPSocket>();
    }


    private void FixedUpdate()
    {   
        if (DebugScript.DebugMode != true){
            y = inputData.y1;
            if (y > this.transform.position.y)
            {
                rb.AddForce(Vector2.up * this.speed);
            }
            else if (y < this.transform.position.y)
            {
                rb.AddForce(Vector2.down * this.speed);
            }


            else if (this.transform.position.y > 0.0f)
            {
                rb.AddForce(Vector2.down * speed);
            }
            else if (this.transform.position.y < 0.0f)
            {
                rb.AddForce(Vector2.up * speed);
            }
        }

        else{
            //Manual Control for debugging
            if (Input.GetKey(KeyCode.W)) {
                rb.AddForce(Vector2.up * this.speed);
            }
            else if (Input.GetKey(KeyCode.S)) {
                rb.AddForce(Vector2.down * this.speed);
            }
        }
        
    }
}
