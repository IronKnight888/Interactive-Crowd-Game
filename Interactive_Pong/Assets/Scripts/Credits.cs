using UnityEngine;
using UnityEngine.SceneManagement;

public class Credits : MonoBehaviour
{
    Rigidbody2D rb;
    private float speed = 0;
    private GameObject button;

    private void Awake()
    {
        rb = gameObject.GetComponent<Rigidbody2D>();
        button = GameObject.FindGameObjectWithTag("Button");
    }

    private void FixedUpdate()
    {
        rb.MovePosition(transform.position + Vector3.up * speed);
    }

    private void OnCollisionEnter2D(Collision2D collision)
    {
        if (collision.gameObject.CompareTag("Wall"))
        {
            print("Switching scenes");
            SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex + 1);
        }
    }
    public void StartMoving()
    {
        speed = 2f;
        button.SetActive(false);
    }
}
