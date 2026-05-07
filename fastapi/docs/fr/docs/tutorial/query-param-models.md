# Modèles de paramètres de requête { #query-parameter-models }

Si vous avez un groupe de paramètres de requête liés, vous pouvez créer un modèle Pydantic pour les déclarer.

Cela vous permet de réutiliser le modèle à plusieurs endroits et aussi de déclarer des validations et des métadonnées pour tous les paramètres en une seule fois. 😎

/// note | Remarque

Pris en charge depuis FastAPI version `0.115.0`. 🤓

///

## Déclarer des paramètres de requête avec un modèle Pydantic { #query-parameters-with-a-pydantic-model }

Déclarez les paramètres de requête dont vous avez besoin dans un modèle Pydantic, puis déclarez le paramètre en tant que `Query` :

{* ../../docs_src/query_param_models/tutorial001_an_py310.py hl[9:13,17] *}

FastAPI extrait les données pour chaque champ à partir des paramètres de requête de la requête et vous fournit le modèle Pydantic que vous avez défini.

## Consulter les documents { #check-the-docs }

Vous pouvez voir les paramètres de requête dans l'interface des documents à `/docs` :

<div class="screenshot">
<img src="/img/tutorial/query-param-models/image01.png">
</div>

## Interdire des paramètres de requête supplémentaires { #forbid-extra-query-parameters }

Dans certains cas d'utilisation particuliers (probablement peu courants), vous pouvez vouloir restreindre les paramètres de requête que vous souhaitez recevoir.

Vous pouvez utiliser la configuration du modèle Pydantic pour `forbid` tout champ `extra` :

{* ../../docs_src/query_param_models/tutorial002_an_py310.py hl[10] *}

Si un client tente d'envoyer des données supplémentaires dans les paramètres de requête, il recevra une réponse d'erreur.

Par exemple, si le client tente d'envoyer un paramètre de requête `tool` avec la valeur `plumbus`, comme :

```http
https://example.com/items/?limit=10&tool=plumbus
```

Il recevra une réponse d'erreur lui indiquant que le paramètre de requête `tool` n'est pas autorisé :

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

## Résumé { #summary }

Vous pouvez utiliser des modèles Pydantic pour déclarer des paramètres de requête dans FastAPI. 😎

/// tip | Astuce

Alerte spoiler : vous pouvez aussi utiliser des modèles Pydantic pour déclarer des cookies et des en-têtes, mais vous lirez cela plus tard dans le tutoriel. 🤫

///
