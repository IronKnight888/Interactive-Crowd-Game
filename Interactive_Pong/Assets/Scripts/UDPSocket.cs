/*
Created by Youssef Elashry to allow two-way communication between Python3 and Unity to send and receive strings

Feel free to use this in your individual or commercial projects BUT make sure to reference me as: Two-way communication between Python 3 and Unity (C#) - Y. T. Elashry
It would be appreciated if you send me how you have used this in your projects (e.g. Machine Learning) at youssef.elashry@gmail.com

Use at your own risk
Use under the Apache License 2.0

Modified by: 
Youssef Elashry 12/2020 (replaced obsolete functions and improved further - works with Python as well)
Based on older work by Sandra Fang 2016 - Unity3D to MATLAB UDP communication - [url]http://msdn.microsoft.com/de-de/library/bb979228.aspx#ID0E3BAC[/url]
*/

using UnityEngine;
using UnityEngine.SceneManagement;
using System.Collections;
using System;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Threading;

public class UDPSocket : MonoBehaviour
{
    public float y1;
    public float y2;
    bool connected;
    private GameObject check;

    [HideInInspector] public bool isTxStarted = false;

    [SerializeField] string IP = "127.0.0.1"; // local host
    [SerializeField] int rxPort = 8000; // port to receive data from Python on
    [SerializeField] int txPort = 8001; // port to send data to Python on

    int i = 0; // DELETE THIS: Added to show sending data from Unity to Python via UDP

    // Create necessary UdpClient objects
    UdpClient client;
    IPEndPoint remoteEndPoint;
    Thread receiveThread; // Receiving Thread

    IEnumerator SendDataCoroutine() // DELETE THIS: Added to show sending data from Unity to Python via UDP
    {
        while (true)
        {
            SendData("Sent from Unity: " + i.ToString());
            i++;
            yield return new WaitForSeconds(1f);
        }
    }

    public void SendData(string message) // Use to send data to Python
    {
        try
        {
            byte[] data = Encoding.UTF8.GetBytes(message);
            client.Send(data, data.Length, remoteEndPoint);
        }
        catch (Exception err)
        {
            print(err.ToString());
        }
    }

    void Awake()
    {
        DontDestroyOnLoad(gameObject);

        check = GameObject.Find("Connection Check");
        check.SetActive(false);
        connected = false;

        y1 = 0;
        y2 = 0;
        // Create remote endpoint (to Matlab) 
        remoteEndPoint = new IPEndPoint(IPAddress.Parse(IP), txPort);

        // Create local client
        client = new UdpClient(rxPort);

        // local endpoint define (where messages are received)
        // Create a new thread for reception of incoming messages
        receiveThread = new Thread(new ThreadStart(ReceiveData));
        receiveThread.IsBackground = true;
        receiveThread.Start();

        // Initialize (seen in comments window)
        print("UDP Comms Initialised");
    }

    private void Update()
    {
        if (connected && SceneManager.GetActiveScene().buildIndex == 1)
        {
            check.SetActive(true);
        }
    }

    // Receive data, update packets received
    private void ReceiveData()
    {
        while (true)
        {
            try
            {
                IPEndPoint anyIP = new IPEndPoint(IPAddress.Any, 0);
                byte[] data = client.Receive(ref anyIP);
                string text = Encoding.UTF8.GetString(data);

                print("connected");
                connected = true;
                calcY(text);
                print(">> " + text);
            }
            catch (Exception err)
            {
                print(err.ToString());
            }
        }
    }

    //Prevent crashes - close clients and threads properly!
    void OnDisable()
    {
        if (receiveThread != null)
            receiveThread.Abort();

        client.Close();
    }
    private void calcY(string data)
    {

        y1 = int.Parse(data.Substring(0, 3));
        y1 = y1 * 7f / 100f - 3.5f; //Scaled from 0 to 100 -> -3.5 to 3.5

        y2 = int.Parse(data.Substring(3, 3));
        y2 = y2 * 7f / 100f - 3.5f; //Scaled from 0 to 100 -> -3.5 to 3.5
    }

}