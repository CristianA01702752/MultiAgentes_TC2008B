using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraSwitch : MonoBehaviour
{

    public GameObject cam1;
    public GameObject cam2;
    public GameObject cam3;
    public GameObject cam4;

    // Update is called once per frame
    void Update()
    {
        if (Input.GetButtonDown("Switch 1"))
        {
            cam1.SetActive(true);
            cam2.SetActive(false);
            cam3.SetActive(false);
            cam4.SetActive(false);
        }
        if (Input.GetButtonDown("Switch 2"))
        {
            cam1.SetActive(false);
            cam2.SetActive(true);
            cam3.SetActive(false);
            cam4.SetActive(false);
        }
        if (Input.GetButtonDown("Switch 3"))
        {
            cam1.SetActive(false);
            cam2.SetActive(false);
            cam3.SetActive(true);
            cam4.SetActive(false);
        }
        if (Input.GetButtonDown("Switch 4"))
        {
            cam1.SetActive(false);
            cam2.SetActive(false);
            cam3.SetActive(false);
            cam4.SetActive(true);
        }

    }
}