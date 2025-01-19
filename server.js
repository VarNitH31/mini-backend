import express from "express";
import bodyParser from "body-parser";
import cors from "cors";
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(bodyParser.json());

app.post("/update", async (req, res) => {
    try {
      const { values, email, predictedJob, interestedJob } = req.body;
  
      // Merge the two objects in the `values` array into one object
      const mergedValues = values.reduce((acc, obj) => ({ ...acc, ...obj }), {});
  
      // Prepare the `userData` object using the merged values
      const userData = {
        emailId: email,
        Communication_skills: mergedValues.Communication_skills || 0,
        Openness: mergedValues.Openness || 0,
        Conscientousness: mergedValues.Conscientousness || 0,
        Extraversion: mergedValues.Extraversion || 0,
        Agreeableness: mergedValues.Agreeableness || 0,
        Emotional_Range: mergedValues.Emotional_Range || 0,
        Conversation: mergedValues.Conversation || 0,
        Openness_to_Change: mergedValues.Openness_to_Change || 0,
        Hedonism: mergedValues.Hedonism || 0,
        Self_enhancement: mergedValues["Self-enhancement"] || 0,
        Self_transcendence: mergedValues["Self-transcendence"] || 0,
        Database_Fundamentals: mergedValues.Database_Fundamentals || 0,
        Computer_Architecture: mergedValues.Computer_Architecture || 0,
        Distributed_Computing_Systems: mergedValues.Distributed_Computing_Systems || 0,
        Cyber_Security: mergedValues.Cyber_Security || 0,
        Networking: mergedValues.Networking || 0,
        Software_Development: mergedValues.Software_Development || 0,
        Programming_Skills: mergedValues.Programming_Skills || 0,
        Project_Management: mergedValues.Project_Management || 0,
        Computer_Forensics_Fundamentals: mergedValues.Computer_Forensics_Fundamentals || 0,
        Technical_Communication: mergedValues.Technical_Communication || 0,
        AI_ML: mergedValues.AI_ML || 0,
        Software_Engineering: mergedValues.Software_Engineering || 0,
        Business_Analysis: mergedValues.Business_Analysis || 0,
        Data_Science: mergedValues.Data_Science || 0,
        Troubleshooting_skills: mergedValues.Troubleshooting_skills || 0,
        Graphics_Designing: mergedValues.Graphics_Designing || 0,
        predictedJob,
        interestedJob,
      };

      const newUser = await prisma.user.create({
        data: userData,
      });
  
      res.status(200).json({
        success: true,
        message: "User created successfully",
        user: newUser,
      });
    } catch (error) {
      console.error("Error creating user:", error);
      res.status(500).json({
        success: false,
        error: "An error occurred while creating the user in the database.",
      });
    }
  });
  
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
