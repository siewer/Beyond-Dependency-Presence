# Header-Parameter-Modelle { #header-parameter-models }

Wenn Sie eine Gruppe verwandter **Header-Parameter** haben, können Sie ein **Pydantic-Modell** erstellen, um diese zu deklarieren.

Dadurch können Sie das **Modell an mehreren Stellen wiederverwenden** und auch Validierungen und Metadaten für alle Parameter gleichzeitig deklarieren. 😎

/// note | Hinweis

Dies wird seit FastAPI Version `0.115.0` unterstützt. 🤓

///

## Header-Parameter mit einem Pydantic-Modell { #header-parameters-with-a-pydantic-model }

Deklarieren Sie die erforderlichen **Header-Parameter** in einem **Pydantic-Modell** und dann den Parameter als `Header`:

{* ../../docs_src/header_param_models/tutorial001_an_py310.py hl[9:14,18] *}

**FastAPI** wird die Daten für **jedes Feld** aus den **Headern** des <abbr title="Request – Anfrage: Daten, die der Client zum Server sendet">Request</abbr> extrahieren und Ihnen das von Ihnen definierte Pydantic-Modell geben.

## Die Dokumentation testen { #check-the-docs }

Sie können die erforderlichen Header in der Dokumentationsoberfläche unter `/docs` sehen:

<div class="screenshot">
<img src="/img/tutorial/header-param-models/image01.png">
</div>

## Zusätzliche Header verbieten { #forbid-extra-headers }

In einigen speziellen Anwendungsfällen (wahrscheinlich nicht sehr häufig) möchten Sie möglicherweise die **Header einschränken**, die Sie erhalten möchten.

Sie können Pydantics Modellkonfiguration verwenden, um `extra` Felder zu verbieten (`forbid`):

{* ../../docs_src/header_param_models/tutorial002_an_py310.py hl[10] *}

Wenn ein Client versucht, einige **zusätzliche Header** zu senden, erhält er eine **Error-<abbr title="Response – Antwort: Daten, die der Server zum anfragenden Client zurücksendet">Response</abbr>**.

Zum Beispiel, wenn der Client versucht, einen `tool`-Header mit einem Wert von `plumbus` zu senden, erhält er eine **Error-Response**, die ihm mitteilt, dass der Header-Parameter `tool` nicht erlaubt ist:

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["header", "tool"],
            "msg": "Extra inputs are not permitted",
            "input": "plumbus",
        }
    ]
}
```

## Automatische Umwandlung von Unterstrichen deaktivieren { #disable-convert-underscores }

Ähnlich wie bei regulären Header-Parametern werden bei der Verwendung von Unterstrichen in den Parameternamen diese **automatisch in Bindestriche umgewandelt**.

Wenn Sie beispielsweise einen Header-Parameter `save_data` im Code haben, wird der erwartete HTTP-Header `save-data` sein, und er wird auch so in der Dokumentation angezeigt.

Falls Sie aus irgendeinem Grund diese automatische Umwandlung deaktivieren müssen, können Sie dies auch für Pydantic-Modelle für Header-Parameter tun.

{* ../../docs_src/header_param_models/tutorial003_an_py310.py hl[19] *}

/// warning | Achtung

Bevor Sie `convert_underscores` auf `False` setzen, bedenken Sie, dass einige HTTP-Proxies und -Server die Verwendung von Headern mit Unterstrichen nicht zulassen.

///

## Zusammenfassung { #summary }

Sie können **Pydantic-Modelle** verwenden, um **Header** in **FastAPI** zu deklarieren. 😎
