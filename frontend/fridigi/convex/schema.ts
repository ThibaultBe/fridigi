import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  fridge: defineTable({
    name: v.string(),
    description: v.string(),
  }),
  ingredient: defineTable({
    fridgeId: v.id("fridge"),
    name: v.string(),
    category: v.string(),
    quantity: v.number(),
  }),
});
