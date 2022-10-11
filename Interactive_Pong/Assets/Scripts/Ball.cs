using UnityEngine;

public class Ball : MonoBehaviour
{
    Rigidbody2D rb;
    AudioManager audioManager;

    public float speed = 200.0f;

    private void Awake()
    {
        rb = GetComponent<Rigidbody2D>();
        audioManager = GameObject.Find("Audio Manager").GetComponent<AudioManager>();
    }

    private void Start()
    {
        ResetPosition();
        AddStartingForce();
    }

    public void AddStartingForce()
    {
        float x = Random.value < 0.5f ? -1.0f : 1.0f;
        float y = Random.value < 0.5f ? Random.Range(-1.0f, -0.5f) : Random.Range(0.5f, 1.0f);

        Vector2 direction = new Vector2(x, y);
        rb.AddForce(direction * this.speed);
    }

    public void AddForce(Vector2 force)
    {
        rb.AddForce(force);
    }

    public void ResetPosition()
    {
        rb.position = Vector3.zero;
        rb.velocity = Vector3.zero;
    }

    private void OnCollisionEnter2D(Collision2D collision)
    {
        if (collision.gameObject.CompareTag("Wall"))
        {
            audioManager.Play("Wall Hit");
        }
        if (collision.gameObject.CompareTag("Paddle"))
        {
            audioManager.Play("Paddle Hit");           
            if (GameModeSetter.GameMode == "Hard" || GameModeSetter.GameMode == "FlashlightHard"){
                Vector2 CurrentDirection = rb.velocity;
                rb.AddForce(CurrentDirection * (this.speed * 0.05f));
            }
            
        }
    }
}
