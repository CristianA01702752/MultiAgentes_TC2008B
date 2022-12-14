using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using UnityEngine.Networking;


public class MoveAgent : MonoBehaviour
{
   public int id;
   public string position;

    IEnumerator Start()
    {
        InvokeRepeating("GetData", 1.0f, 0.89f);
        yield return new WaitForSeconds(300);
        CancelInvoke("GetData");
        
    }

    void GetData ()
    {
        StartCoroutine(GetDataCoroutine());
    }
    
    IEnumerator GetDataCoroutine(){
        string url = "http://localhost:8585/position?id=" + id;
        using (UnityWebRequest www = UnityWebRequest.Get(url))
        {
            yield return www.SendWebRequest();
            if(www.isNetworkError || www.isHttpError)
            {
                Debug.Log(www.error);
                position = www.error;
               

            }
            else
            {
                // Debug.Log(www.downloadHandler.text);
                position= www.downloadHandler.text;
                position = position.TrimStart('[');
                position = position.TrimEnd(']');
                
                string[] positionArray = position.Split(',');
                string x = positionArray[0];
                x= x.TrimStart('{', '"', 'x', '"', ':');
                x= x.TrimEnd(' ');
                int positionX = int.Parse(x);
                //Debug.Log(positionX);

                string z = positionArray[1];
                z= z.TrimStart(' ','"', 'z', '"', ':');
                z= z.TrimEnd(' ');
                int positionZ = int.Parse(z);
                // Debug.Log(positionZ)
                
                // string s = positionArray[4];
                // s = s.TrimStart(' ','"', 's', '"', ':');
                // s = s.TrimEnd(' ');
                // int status_car = int.Parse(s);


                Vector3 currentPosition = transform.position;
                Vector3 targetPos = new Vector3(positionX , 0.0f, positionZ);

                float timeElapsed = 0;
                float timeToMove = 0.9f;
                while (timeElapsed < timeToMove)
                {
                    transform.position = Vector3.Lerp(currentPosition, targetPos, timeElapsed / timeToMove);
                    timeElapsed += Time.deltaTime;
                    yield return null;
                }

            }
        }
    }
}
