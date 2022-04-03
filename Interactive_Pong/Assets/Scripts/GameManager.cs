using System.Collections;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;

public class GameManager : MonoBehaviour
{
    public Ball ball;
    public Text p1_score_text;
    public Text p2_score_text;
    private ScoreTracker scoreTracker;
    private AudioManager audioManager;

    public Paddle p1_paddle;
    public Paddle p2_paddle;

    private int p1_score;
    private int p2_score;

    private int win_num = 3;
    private float wait = 0.5f;


    private void Awake()
    {
        DontDestroyOnLoad(this);
        scoreTracker = GameObject.Find("Score Tracker").GetComponent<ScoreTracker>();
        audioManager = GameObject.Find("Audio Manager").GetComponent<AudioManager>();
    }


    public void LeftScores()
    {
        audioManager.Play("Score");
        p1_score++;
        scoreTracker.p1_score = p1_score;

        this.p1_score_text.text = p1_score.ToString();

        if (p1_score >= win_num)
        {
            scoreTracker.winner = "Left";
            StartCoroutine(WinScreen(wait));
        }

        ResetRound();
    }

    public void RightScores()
    {
        audioManager.Play("Score");
        p2_score++;
        scoreTracker.p2_score = p2_score;

        this.p2_score_text.text = p2_score.ToString();

        if (p2_score >= win_num)
        {
            scoreTracker.winner = "Right";
            StartCoroutine(WinScreen(wait));
        }

        ResetRound();
    }


    public IEnumerator WinScreen(float wait)
    {
        ball.GetComponent<Rigidbody2D>().constraints = RigidbodyConstraints2D.FreezeAll;
        p1_paddle.GetComponent<Rigidbody2D>().constraints = RigidbodyConstraints2D.FreezeAll;
        p2_paddle.GetComponent<Rigidbody2D>().constraints = RigidbodyConstraints2D.FreezeAll;

        yield return new WaitForSeconds(wait);
        SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex + 1);
    }

    private void ResetRound()
    {
        this.p1_paddle.ResetPosition();
        this.p2_paddle.ResetPosition();
        this.ball.ResetPosition();
        this.ball.AddStartingForce();
    }
}
