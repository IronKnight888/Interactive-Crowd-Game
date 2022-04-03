using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;

public class WinManager : MonoBehaviour
{
    private ScoreTracker scoreTracker;
    public Text win_text;

    private void Start()
    {
        scoreTracker = GameObject.Find("Score Tracker").GetComponent<ScoreTracker>();
        this.win_text.text = scoreTracker.winner + " WINS!\n" + scoreTracker.p1_score + " - " + scoreTracker.p2_score;
    }

    public void PlayAgain()
    {
        scoreTracker.p1_score = 0;
        scoreTracker.p2_score = 0;
        SceneManager.LoadScene(2);
    }
}
