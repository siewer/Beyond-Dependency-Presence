ALTER TABLE foo ADD COLUMN "baR" "Mixed Case"
  Default ('foo'::"BarBazBaq") ON UPDATe ('baz':::"With Emojis too 👍"), ADD COLUMN "baR" "DefaultDB"."👎"."Mixed Case"
  Default ('foo'::"DefaultDB".public."Mixed Case") ON UPDATe ('baz':::"👎"."Mixed Case")
