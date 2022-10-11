using UnityEngine;
using UnityEngine.SceneManagement;
using System.Collections;
using System.Collections.Generic;

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
        if (Input.GetKey(KeyCode.Space)) {
            SceneManager.LoadScene("Menu");
        }

        rb.MovePosition(transform.position + Vector3.up * speed);
    }

    private void OnCollisionEnter2D(Collision2D collision)
    {
        if (collision.gameObject.CompareTag("Wall"))
        {
            StartCoroutine(CreditsCoroutine());
        }
    }

    IEnumerator CreditsCoroutine()
    {
        Debug.Log("Started Coroutine at timestamp : " + Time.time);

        yield return new WaitForSeconds(2);

        SceneManager.LoadScene("Menu");

        Debug.Log("Finished Coroutine at timestamp : " + Time.time);
    }


    public void StartMoving()
    {
        speed = 0.03f;
        button.SetActive(false);
    }
}
