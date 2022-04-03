using UnityEngine;

public class LightPaddle2 : Paddle
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
        y = inputData.y2;
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
}
