# Query-Parameter-Modelle { #query-parameter-models }

Wenn Sie eine Gruppe von **Query-Parametern** haben, die miteinander in Beziehung stehen, können Sie ein **Pydantic-Modell** erstellen, um diese zu deklarieren.

Dadurch können Sie das **Modell an mehreren Stellen wiederverwenden** und gleichzeitig Validierungen und Metadaten für alle Parameter auf einmal deklarieren. 😎

/// note | Hinweis

Dies wird seit FastAPI Version `0.115.0` unterstützt. 🤓

///

## Query-Parameter mit einem Pydantic-Modell { #query-parameters-with-a-pydantic-model }

Deklarieren Sie die benötigten **Query-Parameter** in einem **Pydantic-Modell** und dann den Parameter als `Query`:

{* ../../docs_src/query_param_models/tutorial001_an_py310.py hl[9:13,17] *}

**FastAPI** wird die Daten für **jedes Feld** aus den **Query-Parametern** des <abbr title="Request – Anfrage: Daten, die der Client zum Server sendet">Request</abbr> extrahieren und Ihnen das definierte Pydantic-Modell bereitstellen.

## Die Dokumentation testen { #check-the-docs }

Sie können die Query-Parameter in der Dokumentations-Oberfläche unter `/docs` einsehen:

<div class="screenshot">
<img src="/img/tutorial/query-param-models/image01.png">
</div>

## Zusätzliche Query-Parameter verbieten { #forbid-extra-query-parameters }

In einigen speziellen Anwendungsfällen (wahrscheinlich nicht sehr häufig) möchten Sie möglicherweise die Query-Parameter, die Sie empfangen möchten, **beschränken**.

Sie können die Modellkonfiguration von Pydantic verwenden, um jegliche `extra` Felder zu `verbieten`:

{* ../../docs_src/query_param_models/tutorial002_an_py310.py hl[10] *}

Wenn ein Client versucht, einige **zusätzliche** Daten in den **Query-Parametern** zu senden, erhält er eine **Error-<abbr title="Response – Antwort: Daten, die der Server zum anfragenden Client zurücksendet">Response</abbr>**.

Wenn der Client beispielsweise versucht, einen `tool` Query-Parameter mit dem Wert `plumbus` zu senden, wie:

```http
https://example.com/items/?limit=10&tool=plumbus
```

erhält er eine **Error-Response**, die ihm mitteilt, dass der Query-Parameter `tool` nicht erlaubt ist:

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["query", "tool"],
            "msg": "Extra inputs are not permitted",
            "input": "plumbus"
        }
    ]
}
```

## Zusammenfassung { #summary }

Sie können **Pydantic-Modelle** verwenden, um **Query-Parameter** in **FastAPI** zu deklarieren. 😎

/// tip | Tipp

Spoiler-Alarm: Sie können auch Pydantic-Modelle verwenden, um Cookies und Header zu deklarieren, aber darüber werden Sie später im Tutorial lesen. 🤫

///
