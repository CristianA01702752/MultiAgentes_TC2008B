using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Threading;

public class SignChange : MonoBehaviour
{
    // Start is called before the first frame update
    int sleepfor = 12000;
    void Start()
    {
        Thread.Sleep(sleepfor);
        Material mymat = GetComponent<Renderer>().material;
        mymat.SetColor("_EmissionColor", Color.blue);
        
    }

    // Update is called once per frame
    void Update()
    {
      
        
        
    }
}
